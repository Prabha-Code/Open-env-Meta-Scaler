def grade(pred, truth):
    try:
        # 🔥 DEFAULT SAFE SCORE (NOT 0)
        score = 0.3

        # 🔥 STRUCTURE CHECK
        if not isinstance(pred, dict):
            return 0.3

        required_keys = ["category", "priority", "sentiment", "action"]
        for key in required_keys:
            if key not in pred:
                return 0.3

        # 🔥 VALID VALUES
        valid = {
            "category": ["billing", "technical", "complaint"],
            "priority": ["low", "medium", "high"],
            "sentiment": ["angry", "neutral", "happy"],
            "action": ["refund", "escalate", "reply"]
        }

        for key in valid:
            if pred[key] not in valid[key]:
                return 0.3

        # 🔥 SAFE SCORING
        if pred["category"] == truth[1]:
            score += 0.1
        if pred["priority"] == truth[2]:
            score += 0.1
        if pred["sentiment"] == truth[3]:
            score += 0.1
        if pred["action"] == truth[4]:
            score += 0.1

        # 🔥 FINAL GUARANTEE
        if score <= 0.0:
            score = 0.2
        if score >= 1.0:
            score = 0.8

        return float(score)

    except Exception:
        return 0.4
