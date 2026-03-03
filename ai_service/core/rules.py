BULLYING_KEYWORDS = {
    "stupid": "harassment",
    "idiot": "harassment",
    "useless": "harassment",
    "kill": "threat",
    "die": "threat"
}

def rule_based_detection(text: str):
    found = []
    for word, category in BULLYING_KEYWORDS.items():
        if word in text:
            found.append(category)
    return found
