from pydantic import BaseModel

class Observation(BaseModel):
    ticket: str

class Action(BaseModel):
    category: str      # billing / technical / complaint
    priority: str      # low / medium / high
    sentiment: str     # angry / neutral / happy
    action: str        # refund / escalate / reply

class Reward(BaseModel):
    score: float
