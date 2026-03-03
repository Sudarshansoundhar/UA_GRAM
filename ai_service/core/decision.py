def decide_action(score: float):
    if score >= 0.75:
        return {
            "severity": "HIGH",
            "action": "block_and_flag",
            "reason": "Severe bullying detected"
        }
    elif score >= 0.4:
        return {
            "severity": "MEDIUM",
            "action": "warn_user",
            "reason": "Potential harassment detected"
        }
    else:
        return {
            "severity": "LOW",
            "action": "allow",
            "reason": "Content appears safe"
        }
