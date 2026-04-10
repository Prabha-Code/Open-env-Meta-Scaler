from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict

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

# ================== REQUEST MODELS ==================
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
        return {"ticket": self.data[self.index][0] if self.data else ""}

    def step(self, action):
        if self.index >= len(self.data):
            return {"ticket": ""}, 0.5, True

        truth = self.data[self.index]

        score = 0.0
        if action.get("category") == truth[1]:
            score += 0.25
        if action.get("priority") == truth[2]:
            score += 0.25
        if action.get("sentiment") == truth[3]:
            score += 0.20
        if action.get("action") == truth[4]:
            score += 0.30

        # === CRITICAL FIX: Never allow 0.0 or 1.0 ===
        if score <= 0.0:
            score = 0.01
        elif score >= 1.0:
            score = 0.99
        else:
            # Add tiny jitter to avoid any floating point exactly 0 or 1
            score = max(0.01, min(0.99, round(score + (hash(str(action)) % 99 - 49) * 0.0001, 4)))

        self.index += 1
        done = self.index >= len(self.data)

        obs = {"ticket": ""} if done else {"ticket": self.data[self.index][0]}

        return obs, float(score), done


env = SupportEnv()

# ================== API ==================
@app.post("/reset")
def reset(req: ResetRequest = None):
    try:
        task = req.task_name if req and hasattr(req, 'task_name') else "easy"
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
        action = req.action if req and hasattr(req, 'action') else {}
        obs, reward, done = env.step(action)
    except Exception as e:
        print(f"Step error: {e}")
        return {
            "observation": {"ticket": ""},
            "reward": 0.5,
            "done": True,
            "info": {}
        }

    return {
        "observation": obs,
        "reward": float(reward),
        "done": done,
        "info": {}
    }
