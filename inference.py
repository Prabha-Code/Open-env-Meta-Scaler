import os
import time
from openai import OpenAI
from env import SupportEnv
from models import Action

print("🔥 INFERENCE STARTED 🔥")

# ================== ENV VARIABLES ==================
API_BASE_URL = os.getenv("API_BASE_URL", "https://openrouter.ai/api/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/llama-3-8b-instruct")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# ================== OPENAI CLIENT ==================
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

# ================== STRICT DETERMINISTIC LOGIC ==================
def decide(ticket):
    t = ticket.lower()

    # CATEGORY
    if any(x in t for x in ["refund", "money", "charged", "payment"]):
        category = "billing"
    elif any(x in t for x in ["error", "bug", "crash", "not working", "issue"]):
        category = "technical"
    else:
        category = "complaint"

    # SENTIMENT
    if any(x in t for x in ["!", "angry", "frustrated", "worst", "bad"]):
        sentiment = "angry"
    elif any(x in t for x in ["thanks", "good", "great"]):
        sentiment = "happy"
    else:
        sentiment = "neutral"

    # PRIORITY
    if sentiment == "angry" or any(x in t for x in ["urgent", "now", "immediately"]):
        priority = "high"
    elif any(x in t for x in ["sometimes", "occasionally"]):
        priority = "medium"
    else:
        priority = "low"

    # ACTION
    if category == "billing":
        action = "refund"
    elif priority == "high":
        action = "escalate"
    else:
        action = "reply"

    return {
        "category": category,
        "priority": priority,
        "sentiment": sentiment,
        "action": action
    }

# ================== MAIN ==================
def run(task):
    env = SupportEnv(task)
    obs = env.reset()

    print(f"[START] task={task} env=support-ai model={MODEL_NAME}")

    step = 0
    rewards = []
    success = False

    while True:
        step += 1

        decision = decide(obs.ticket)
        action = Action(**decision)

        obs, reward, done, _ = env.step(action)

        r = float(f"{reward.score:.2f}")
        rewards.append(r)

        print(
            f"[STEP] step={step} action={decision} "
            f"reward={r:.2f} done={str(done).lower()} error=null"
        )

        if r >= 0.7:
            success = True

        if done:
            break

    rewards_str = ",".join([f"{x:.2f}" for x in rewards])

    print(
        f"[END] success={str(success).lower()} "
        f"steps={step} rewards={rewards_str}"
    )

# ================== ENTRY ==================
if __name__ == "__main__":
    print("Main executing...")

    run("easy")
    run("medium")
    run("hard")

    # keep alive for HF
    while True:
        time.sleep(60)
