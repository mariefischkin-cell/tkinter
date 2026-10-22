"""
Spam Shield - NLP Activity 1 (full solution)
Grades 8-12 | 30 minutes | Python 3, standard library only

Real world: Gmail, Outlook and SMS apps give every message a score
and move risky ones to the spam folder. We build a simple version.
"""

# ---------------------------------------------------------------
# Step 1: Spam words and how "spammy" each one is (its weight)
# ---------------------------------------------------------------
SPAM_WORDS = {
    "free": 2, "winner": 3, "won": 3, "prize": 3, "lottery": 3,
    "urgent": 2, "click": 2, "claim": 2, "cash": 2, "verify": 2,
    "congratulations": 2, "offer": 1, "limited": 1, "now": 1, "account": 1,
}

THRESHOLD = 4       # a score at or above this means SPAM
USE_LEET = False    # "Break it" step: set to True to catch W1NNER, cl1ck, pr1ze

LEET = str.maketrans("13450@$", "ieasoas")   # 1->i, 3->e, 4->a, 5->s, 0->o, @->a, $->s
PUNCTUATION = ".,!?:;\"'()"


# ---------------------------------------------------------------
# Step 2: Clean one word, then split a message into clean words
# ---------------------------------------------------------------
def clean_word(word):
    word = word.lower()
    if USE_LEET:
        word = word.translate(LEET)
    return word.strip(PUNCTUATION)


def tokenize(message):
    words = []
    for word in message.split():
        cleaned = clean_word(word)
        if cleaned:
            words.append(cleaned)
    return words


# ---------------------------------------------------------------
# Step 3: Add up the weights of every spam word in the message
# ---------------------------------------------------------------
def spam_score(message):
    score = 0
    for word in tokenize(message):
        score += SPAM_WORDS.get(word, 0)
    return score


# ---------------------------------------------------------------
# Step 4: Decide SPAM or SAFE, and explain which words were flagged
# ---------------------------------------------------------------
def classify(message):
    if spam_score(message) >= THRESHOLD:
        return "SPAM"
    return "SAFE"


def explain(message):
    return [word for word in tokenize(message) if word in SPAM_WORDS]


# ---------------------------------------------------------------
# Step 5: Test on messages where we already know the right answer
# ---------------------------------------------------------------
TEST_MESSAGES = [
    ("Congratulations! You WON a free iPhone. Click now to claim", "SPAM"),
    ("URGENT: verify your account or it will be blocked", "SPAM"),
    ("Claim your cash prize before midnight", "SPAM"),
    ("Hey, are we still meeting at 5?", "SAFE"),
    ("Your free coding class starts at 5 PM today", "SAFE"),
    ("Mom says dinner is ready, come down now", "SAFE"),
    ("W1NNER!!! cl1ck here for your pr1ze", "SPAM"),
    ("Limited offer: free cash for new users, claim now", "SPAM"),
    ("Click the link in the class group to join the free quiz now", "SAFE"),
    ("Your bank account statement for March is ready", "SAFE"),
]


def run_tests():
    correct = false_positives = false_negatives = 0
    for message, expected in TEST_MESSAGES:
        result = classify(message)
        if result == expected:
            correct += 1
            mark = "OK"
        elif result == "SPAM":
            false_positives += 1
            mark = "FP"   # a safe message wrongly blocked
        else:
            false_negatives += 1
            mark = "FN"   # spam that slipped through
        print(f"{mark}  {result}  score={spam_score(message):>2}  {message}")
    print(f"\nAccuracy: {correct}/{len(TEST_MESSAGES)}")
    print(f"False positives (safe messages blocked): {false_positives}")
    print(f"False negatives (spam that got through): {false_negatives}")


# ---------------------------------------------------------------
# Step 6: Check any message live
# ---------------------------------------------------------------
if __name__ == "__main__":
    run_tests()
    print("\nType a message to check it, or 'quit' to stop.")
    while True:
        message = input("\n> ")
        if message.strip().lower() == "quit":
            break
        print(f"{classify(message)} | score: {spam_score(message)} | flagged: {explain(message)}")
