from fastapi import FastAPI
from pydantic import BaseModel

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
    task_name: str   # 🔥 FIXED

class StepRequest(BaseModel):
    action: dict

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
        try:
            truth = self.data[self.index]
        except:
            return {"ticket": ""}, 0.0, True

        score = 0.0

        if action.get("category") == truth[1]:
            score += 0.25
        if action.get("priority") == truth[2]:
            score += 0.25
        if action.get("sentiment") == truth[3]:
            score += 0.2
        if action.get("action") == truth[4]:
            score += 0.3

        self.index += 1
        done = self.index >= len(self.data)

        obs = {"ticket": ""} if done else {"ticket": self.data[self.index][0]}

        return obs, float(score), done

env = SupportEnv()

# ================== API ==================
@app.post("/reset")
def reset(req: ResetRequest):
    obs = env.reset(req.task_name)

    return {
        "observation": obs,
        "info": {}
    }

@app.post("/step")
def step(req: StepRequest):
    try:
        obs, reward, done = env.step(req.action)
    except Exception:
        return {
            "observation": {"ticket": ""},
            "reward": 0.0,
            "done": True,
            "info": {}
        }

    return {
        "observation": obs,
        "reward": float(reward),
        "done": done,
        "info": {}
    }
