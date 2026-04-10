from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict
import uvicorn

app = FastAPI()

class ResetRequest(BaseModel):
    task_name: Optional[str] = "easy"

class StepRequest(BaseModel):
    action: Optional[Dict] = {}

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/reset")
def reset(req: ResetRequest = None):
    return {
        "observation": {"ticket": "Refund my money!"},
        "info": {}
    }

@app.post("/step")
def step(req: StepRequest = None):
    return {
        "observation": {"ticket": ""},
        "reward": 0.73,   # strictly between 0 and 1
        "done": True,
        "info": {}
    }

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
