
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
import json

analyzer = SentimentIntensityAnalyzer()
history = []

def analyze(text):
    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    entry = {
        "text": text,
        "sentiment": sentiment,
        "score": round(compound, 3),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    history.append(entry)
    print(f"\nSentiment: {sentiment}")
    print(f"Confidence score: {compound:.3f}")
    return entry

def statistics():
    total = len(history)
    print("\n--- SENTIMENT STATISTICS ---")
    print("Total messages:", total)

    for sentiment in ["Positive", "Negative", "Neutral"]:
        count = sum(
            item["sentiment"] == sentiment
            for item in history
        )
        percentage = (count / total * 100) if total else 0
        print(f"{sentiment}: {count} ({percentage:.1f}%)")

def show_history():
    if not history:
        print("No conversation history.")
        return

    for index, item in enumerate(history, 1):
        print(
            f'{index}. [{item["sentiment"]}] '
            f'{item["text"]} ({item["score"]})'
        )

def save_report():
    statistics()

    report = {
        "generated_at": datetime.now().isoformat(),
        "total_messages": len(history),
        "statistics": {
            sentiment: sum(
                item["sentiment"] == sentiment
                for item in history
            )
            for sentiment in ["Positive", "Negative", "Neutral"]
        },
        "conversation_history": history
    }

    with open("sentiment_report.json", "w") as file:
        json.dump(report, file, indent=4)

    with open("sentiment_report.txt", "w") as file:
        file.write("SENTIMENT SPY - MISSION REPORT\n")
        file.write("=" * 35 + "\n")

        for sentiment, count in report["statistics"].items():
            file.write(f"{sentiment}: {count}\n")

        file.write("\nCONVERSATION HISTORY\n")

        for item in history:
            file.write(
                f'{item["time"]} | {item["sentiment"]} | '
                f'{item["text"]}\n'
            )

    print("\nMission report saved successfully!")

print("=== SENTIMENT SPY ===")
print("Enter an English sentence to analyze.")
print("Commands: stats, history, reset, report, exit")

while True:
    user_input = input("\nYou: ").strip()

    if not user_input:
        continue

    command = user_input.lower()

    if command == "stats":
        statistics()

    elif command == "history":
        show_history()

    elif command == "reset":
        history.clear()
        print("All data has been reset.")

    elif command == "report":
        save_report()

    elif command == "exit":
        save_report()
        print("Mission completed. Goodbye!")
        break

    else:
        analyze(user_input)
