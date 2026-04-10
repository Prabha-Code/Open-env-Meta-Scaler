def grade(pred, truth):
    try:
        # 🔥 Validate structure
        if not isinstance(pred, dict):
            return 0.2   # ❌ NOT 0.0

        required_keys = ["category", "priority", "sentiment", "action"]
        for key in required_keys:
            if key not in pred:
                return 0.2   # ❌ NOT 0.0

        # 🔥 Valid values
        valid = {
            "category": ["billing", "technical", "complaint"],
            "priority": ["low", "medium", "high"],
            "sentiment": ["angry", "neutral", "happy"],
            "action": ["refund", "escalate", "reply"]
        }

        # 🔥 Check validity
        for key in valid:
            if pred[key] not in valid[key]:
                return 0.2   # ❌ NOT 0.0

        # 🔥 SAFE SCORING (NO 0 / NO 1)
        score = 0.2   # 🔥 START SAFE

        if pred["category"] == truth[1]:
            score += 0.2
        if pred["priority"] == truth[2]:
            score += 0.2
        if pred["sentiment"] == truth[3]:
            score += 0.15
        if pred["action"] == truth[4]:
            score += 0.15

        # 🔥 FINAL GUARANTEE
        if score <= 0.0:
            score = 0.2
        if score >= 1.0:
            score = 0.9

        return float(score)

    except Exception:
        return 0.3   # ❌ NOT 0.0
