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
    task: str

class StepRequest(BaseModel):
    action: dict

# ================== ENV CLASS ==================
class SupportEnv:
    def __init__(self):
        self.task = None
        self.data = []
        self.index = 0

    def reset(self, task):
        self.task = task
        self.data = DATA[task]
        self.index = 0

        return {
            "ticket": self.data[self.index][0]
        }

    def step(self, action):
        truth = self.data[self.index]

        score = 0.0
        if action["category"] == truth[1]:
            score += 0.25
        if action["priority"] == truth[2]:
            score += 0.25
        if action["sentiment"] == truth[3]:
            score += 0.2
        if action["action"] == truth[4]:
            score += 0.3

        self.index += 1
        done = self.index >= len(self.data)

        obs = {"ticket": ""} if done else {"ticket": self.data[self.index][0]}

        return obs, score, done

env = SupportEnv()

# ================== API ==================
@app.post("/reset")
def reset(req: ResetRequest):
    obs = env.reset(req.task)
    return obs

@app.post("/step")
def step(req: StepRequest):
    obs, reward, done = env.step(req.action)
    return {
        "obs": obs,
        "reward": reward,
        "done": done
    }
