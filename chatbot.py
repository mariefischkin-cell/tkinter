
import random
import re
from datetime import datetime

class SmartChatbot:
    def __init__(self):
        self.name = "Cody"
        self.user_name = None
        self.memory = {}
        self.running = True

        self.responses = {
            "greeting": [
                "Hello! How can I help you?",
                "Hi there! What would you like to do?",
                "Hey! Nice to meet you!"
            ],
            "how_are_you": [
                "I'm doing great! Thanks for asking.",
                "I'm ready to help you!",
                "Everything is working perfectly!"
            ],
            "thanks": [
                "You're welcome!",
                "No problem!",
                "Happy to help!"
            ],
            "goodbye": [
                "Goodbye! Have a great day!",
                "See you next time!",
                "Bye! Keep learning Python!"
            ]
        }

    def detect_intent(self, message):
        text = message.lower().strip()

        if re.search(r"\b(bye|goodbye|exit|quit)\b", text):
            return "goodbye"

        if re.search(r"\b(hello|hi|hey)\b", text):
            return "greeting"

        if "how are you" in text:
            return "how_are_you"

        if re.search(r"\b(thanks|thank you)\b", text):
            return "thanks"

        if "your name" in text:
            return "bot_name"

        if "my name" in text:
            return "user_name"

        if "time" in text:
            return "time"

        if "date" in text:
            return "date"

        if "help" in text:
            return "help"

        if "python" in text:
            return "python"

        if "joke" in text:
            return "joke"

        if "remember" in text:
            return "memory"

        return "unknown"

    def respond(self, message):
        text = message.strip()
        lower = text.lower()

        name_match = re.search(
            r"(?:my name is|call me)\s+([a-zA-Z]+)",
            text,
            re.IGNORECASE
        )

        if name_match:
            self.user_name = name_match.group(1).capitalize()
            return f"Nice to meet you, {self.user_name}!"

        intent = self.detect_intent(message)

        if intent in self.responses:
            if intent == "goodbye":
                self.running = False
            return random.choice(self.responses[intent])

        if intent == "bot_name":
            return f"My name is {self.name}, your Python chatbot!"

        if intent == "user_name":
            if self.user_name:
                return f"Your name is {self.user_name}."
            return "I don't know your name yet. Tell me!"

        if intent == "time":
            return datetime.now().strftime(
                "The current time is %H:%M:%S"
            )

        if intent == "date":
            return datetime.now().strftime(
                "Today is %B %d, %Y"
            )

        if intent == "help":
            return (
                "You can ask me about Python, time, date, "
                "jokes, or tell me your name."
            )

        if intent == "python":
            return (
                "Python is a powerful programming language "
                "used for AI, automation, and applications."
            )

        if intent == "joke":
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "Why did the Python developer wear glasses? Because they couldn't C!",
                "There are 10 types of people: those who understand binary and those who don't."
            ]
            return random.choice(jokes)

        if lower.startswith("remember "):
            information = text[9:].strip()
            self.memory["note"] = information
            return "Okay! I will remember that during this chat."

        if "what do you remember" in lower:
            return self.memory.get(
                "note", "I don't remember anything yet."
            )

        return (
            "I'm not sure how to answer that yet. "
            "Try asking something else!"
        )

    def start(self):
        print("=" * 45)
        print("SMART RULE-BASED CHATBOT")
        print("=" * 45)
        print("Type 'help' for available commands.")
        print("Type 'bye' to exit.\n")

        while self.running:
            try:
                message = input("You: ")

                if not message.strip():
                    continue

                response = self.respond(message)
                print("Cody:", response)

            except (KeyboardInterrupt, EOFError):
                print("\nCody: Goodbye!")
                break

if __name__ == "__main__":
    chatbot = SmartChatbot()
    chatbot.start()
