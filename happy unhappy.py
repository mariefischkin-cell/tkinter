
positive_words = {
    "good": 2,
    "great": 3,
    "delicious": 3,
    "nice": 2,
    "fresh": 2,
    "love": 3,
    "tasty": 2
}

negative_words = {
    "bad": -2,
    "terrible": -3,
    "cold": -2,
    "awful": -3,
    "hate": -3,
    "dirty": -2,
    "slow": -1
}

def predict(comment):
    words = comment.lower().split()
    score = 0

    for word in words:
        word = word.strip(".,!?")
        score += positive_words.get(word, 0)
        score += negative_words.get(word, 0)

    if "not" in words:
        score = -score

    if score > 0:
        return "HAPPY"
    elif score < 0:
        return "UNHAPPY"
    return "OK"

comments = [
    "The food is delicious",
    "The lunch was terrible",
    "The food is okay",
    "I love the fresh food",
    "The soup is not good"
]

for comment in comments:
    print(comment, "->", predict(comment))
