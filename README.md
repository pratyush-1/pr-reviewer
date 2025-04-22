**PROJECT OVERVIEW**
AI bot that reviews GitHub PRs using Ollama. Checks code safety and auto-merges clean changes.

Download Ollama from [here](!https://ollama.com/download/windows)

The project is structured as follows- 

```
pr-reviewer/
├── app/
│   ├── main.py          
│   ├── github_webhook.py 
│   ├── llm_langchain.py  
│   └── utils.py          
├── .env                
└── requirements.txt     
```
## Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/pr-reviewer.git
   cd pr-reviewer
   pip install -r requirements.txt
   ```
2. **Create a .env file which has** - 
    ``` 
    GITHUB_TOKEN = ghp_yourtokenhere
    REPO_NAME = yourusername/yourrepo
    MODEL_NAME = mistral (change this depending on the model)
    OLLAMA_BASE_URL = http://localhost:11434
    ```
3. **Github Webhook Configuration** - 
       Go to your repository-> Settings -> Webhooks 
       for payload URL --> use ``` ngrok http 8000``` and copy the URL in front of forwarding.
       Content type: application/json
       Event: Pull requests
4. **Run the bot**
    ```
    uvicorn app.main:app --reload --port 8000
    ```
5. **TESTING**:
    Create a new branch and then submit a pull request in that branch. The bot will now give reviews and based on the review it will merge.