from fastapi import FastAPI
from app.github_webhook import router as webhook_router

app = FastAPI()
app.include_router(webhook_router)