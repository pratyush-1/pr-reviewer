from fastapi import APIRouter, Request
from app.utils import get_pr_diff, post_pr_comment, merge_pull_request
from app.llm_langchain import review_code

router = APIRouter()

@router.post("/webhook")
async def github_webhook(request: Request):
    try:
        payload = await request.json()
        # print(payload)
        action = payload.get("action")
        print(f'received_action {action}')
        if action not in ["opened", "synchronize"]:
            print("Ignoring action:", action)
            return {"msg": f"Ignoring action: {action}"}

        pr_number = payload["pull_request"]["number"]
        repo_full_name = payload["repository"]["full_name"]

        print(f"Reviewing PR #{pr_number} in {repo_full_name}")

        # Get diff of PR
        diff = get_pr_diff(repo_full_name, pr_number)
        review = review_code(diff)
        print(review)
        post_pr_comment(repo_full_name,pr_number,f"AI Suggestion: {review}")

        approval_keywords = ["looks good","approved","no issues","ready to merge","[approve]","merge this",
            "lgtm", "good to go", "seems fine", "no problems", "no concerns"]
        if any(keyword in review.lower() for keyword in approval_keywords):
            try:
                merge_pull_request(repo_full_name, pr_number)
                post_pr_comment(repo_full_name, pr_number, "PR was automatically merged by the AI Reviewer Bot.")
                return {"message": "Reviewed and merged"}
            except Exception as merge_error:
                post_pr_comment(repo_full_name, pr_number, f"Bot tried to merge but failed: {merge_error}")
                return {"message":"Reviewed but merge failed"}
        
        return {"message":"Reviewed but not merged"}
    except Exception as e:
        return {"error":str(e)}