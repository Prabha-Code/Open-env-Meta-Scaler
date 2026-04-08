def grade(pred, truth):
    try:
        # 🔥 Validate structure
        if not isinstance(pred, dict):
            return 0.0

        required_keys = ["category", "priority", "sentiment", "action"]
        for key in required_keys:
            if key not in pred:
                return 0.0

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
                return 0.0

        # 🔥 Safe scoring
        score = 0.0

        if pred["category"] == truth[1]:
            score += 0.25
        if pred["priority"] == truth[2]:
            score += 0.25
        if pred["sentiment"] == truth[3]:
            score += 0.2
        if pred["action"] == truth[4]:
            score += 0.3

        # 🔥 Clamp (VERY IMPORTANT)
        score = max(0.0, min(1.0, score))

        return float(score)

    except Exception:
        return 0.0
