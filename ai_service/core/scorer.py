def calculate_score(text, categories, previous_flags):
    base_score = 0.0

    if categories:
        base_score += 0.4

    if "threat" in categories:
        base_score += 0.4

    base_score += min(previous_flags * 0.1, 0.3)

    return min(base_score, 1.0), list(set(categories))
