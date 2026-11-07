
urgent_words = {
    "urgent": 5,
    "immediately": 4,
    "emergency": 5,
    "broken": 3,
    "cancel": 2,
    "late": 2,
    "missing": 3,
    "wrong": 2,
    "refund": 2,
    "today": 1
}

def classify_message(message):
    score = 0
    words = message.lower().split()

    for word in words:
        word = word.strip(".,!?")
        score += urgent_words.get(word, 0)

    if score >= 3:
        return "URGENT"
    return "NORMAL"


messages = [
    ("My order is missing", "URGENT"),
    ("What time do you open?", "NORMAL"),
    ("I need an urgent refund", "URGENT"),
    ("Do you sell chocolate cake?", "NORMAL"),
    ("The delivery is late today", "URGENT"),
    ("Thank you for the delicious bread", "NORMAL"),
    ("My cake arrived broken", "URGENT"),
    ("Can I order bread tomorrow?", "NORMAL")
]

mistakes = 0

for message, correct_answer in messages:
    prediction = classify_message(message)

    print("Message:", message)
    print("Prediction:", prediction)
    print("Correct:", correct_answer)

    if prediction != correct_answer:
        mistakes += 1
        print("Result: WRONG")
    else:
        print("Result: CORRECT")

    print()

print("Total messages:", len(messages))
print("Total mistakes:", mistakes)
print("Accuracy:", round(
    (len(messages) - mistakes) / len(messages) * 100, 2
), "%")
