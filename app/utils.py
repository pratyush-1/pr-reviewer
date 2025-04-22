import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_API = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "User-agent": "PR-Reviewer-Bot/1.0"
}

def get_pr_diff(repo: str, pr_number: int) -> str:
    url = f"{GITHUB_API}/repos/{repo}/pulls/{pr_number}"
    diff_headers = HEADERS.copy()
    diff_headers["Accept"] = "application/vnd.github.v3.diff"

    response = requests.get(url, headers=diff_headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch PR diff: {response.status_code} - {response.text}")

    return response.text

def post_pr_comment(repo: str, pr_number: int, comment: str)  -> None:

    url = f"{GITHUB_API}/repos/{repo}/issues/{pr_number}/comments"
    data = {"body":comment}

    try:
        print(f"Attempting to post comment to PR #{pr_number}")  
        response = requests.post(url, headers=HEADERS, json=data)
        response.raise_for_status()  
        print(f"Successfully posted comment: {response.json()}")  
        return response.json()
    except Exception as e:
        print(f"CRITICAL: Failed to post comment: {str(e)}") 
        print(f"Response content: {e.response.text if hasattr(e, 'response') else 'None'}")
        raise  # Re-raise the exception to stop execution

def merge_pull_request(repo: str, pr_number: int, commit_message: str = "Auto-merged by AI reviewer"):
    url = f"{GITHUB_API}/repos/{repo}/pulls/{pr_number}/merge"
    payload = {
        "commit_title": commit_message,
        "merge_method":"merge",
    }
    response = requests.put(url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        print(f"PR #{pr_number} merged successfully.")
        return response.json()
    elif response.status_code == 405:
        raise Exception(f"Merge conflict — cannot merge PR #{pr_number}.")
    else:
        raise Exception(f"Failed to merge PR: {response.status_code} - {response.text}")