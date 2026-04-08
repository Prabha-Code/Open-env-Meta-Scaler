from models import Observation, Action, Reward
from tasks import TASKS

class SupportEnv:
    def __init__(self, difficulty="easy"):
        self.data = TASKS[difficulty]
        self.index = 0

    def reset(self):
        self.index = 0
        return Observation(ticket=self.data[self.index][0])

    def step(self, action: Action):
        correct = self.data[self.index]

        score = 0.0

        # 🔥 reward shaping (VERY IMPORTANT)
        if action.category == correct[1]:
            score += 0.25
        if action.priority == correct[2]:
            score += 0.25
        if action.sentiment == correct[3]:
            score += 0.2
        if action.action == correct[4]:
            score += 0.3

        self.index += 1
        done = self.index >= len(self.data)

        obs = None if done else Observation(ticket=self.data[self.index][0])

        return obs, Reward(score=score), done, {"correct": correct}

    def state(self):
        return {"index": self.index}
