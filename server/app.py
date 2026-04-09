from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict
import uvicorn

app = FastAPI()

# ================== DATA ==================
DATA = {
    "easy": [
        ("Refund my money!", "billing", "high", "angry", "refund"),
        ("App not working", "technical", "medium", "neutral", "escalate")
    ],
    "medium": [
        ("Charged twice!", "billing", "high", "angry", "refund"),
        ("Bug in dashboard", "technical", "medium", "neutral", "escalate")
    ],
    "hard": [
        ("Worst service ever!", "complaint", "high", "angry", "escalate"),
        ("Payment failed again", "billing", "high", "angry", "refund")
    ]
}

# ================== MODELS ==================
class ResetRequest(BaseModel):
    task_name: Optional[str] = "easy"

class StepRequest(BaseModel):
    action: Optional[Dict] = {}

# ================== ENV ==================
class SupportEnv:
    def __init__(self):
        self.data = []
        self.index = 0

    def reset(self, task):
        self.data = DATA.get(task, DATA["easy"])
        self.index = 0
        return {"ticket": self.data[self.index][0]}

    def step(self, action):
        # 🔥 DEFAULT SAFE VALUES
        score = 0.5
        done = False
        obs = {"ticket": ""}

        try:
            # END CASE
            if self.index >= len(self.data):
                return {"ticket": ""}, 0.5, True

            truth = self.data[self.index]

            # 🔥 SAFE START (NEVER 0)
            score = 0.3

            if action and action.get("category") == truth[1]:
                score += 0.1
            if action and action.get("priority") == truth[2]:
                score += 0.1
            if action and action.get("sentiment") == truth[3]:
                score += 0.1
            if action and action.get("action") == truth[4]:
                score += 0.1

            self.index += 1
            done = self.index >= len(self.data)

            obs = {"ticket": ""} if done else {"ticket": self.data[self.index][0]}

        except Exception:
            return {"ticket": ""}, 0.5, True

        # 🔥 FINAL HARD GUARANTEE (NO 0 / NO 1)
        if score <= 0.0:
            score = 0.1
        elif score >= 1.0:
            score = 0.9

        return obs, float(score), done

env = SupportEnv()

# ================== ROUTES ==================
@app.get("/")
def home():
    return {"status": "🚀 OpenEnv API Running"}

@app.post("/reset")
def reset(req: ResetRequest = None):
    try:
        task = req.task_name if req else "easy"
    except:
        task = "easy"

    obs = env.reset(task)

    return {
        "observation": obs,
        "info": {}
    }

@app.post("/step")
def step(req: StepRequest = None):
    try:
        action = req.action if req else {}
        obs, reward, done = env.step(action)
    except Exception:
        return {
            "observation": {"ticket": ""},
            "reward": 0.5,
            "done": True,
            "info": {}
        }

    # 🔥 FINAL RESPONSE SAFE
    if reward <= 0.0:
        reward = 0.1
    elif reward >= 1.0:
        reward = 0.9

    return {
        "observation": obs,
        "reward": float(reward),
        "done": done,
        "info": {}
    }

# ================== MAIN ==================
def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
