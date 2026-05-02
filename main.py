from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.reddit import fetch_reddit_posts
from services.ai import generate_viral_hooks
from services.scoring import score_and_rank_hooks
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
def test_endpoint():
    return {"status": "working"}

@app.get("/posts")
def get_posts(niche: str):
    posts = fetch_reddit_posts(niche)
    return {
        "niche": niche,
        "posts": posts
    }

@app.get("/hooks")
def get_hooks(niche: str):
    posts = fetch_reddit_posts(niche)
    hooks = generate_viral_hooks(posts)
    ranked_hooks = score_and_rank_hooks(hooks)
    return {
        "niche": niche,
        "hooks": ranked_hooks
    }

# To run the server, execute this command from the 'backend' directory:
# uvicorn main:app --reload
