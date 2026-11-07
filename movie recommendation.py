
import random

movies = [
    {
        "title": "Interstellar",
        "genre": "Sci-Fi",
        "mood": "Thoughtful",
        "rating": 8.7,
        "overview": "An amazing and emotional journey through space."
    },
    {
        "title": "The Dark Knight",
        "genre": "Action",
        "mood": "Exciting",
        "rating": 9.0,
        "overview": "A thrilling story about a hero facing dangerous enemies."
    },
    {
        "title": "Inside Out",
        "genre": "Animation",
        "mood": "Happy",
        "rating": 8.1,
        "overview": "A wonderful and emotional adventure about feelings."
    },
    {
        "title": "Inception",
        "genre": "Sci-Fi",
        "mood": "Thoughtful",
        "rating": 8.8,
        "overview": "A fascinating adventure inside dreams."
    },
    {
        "title": "Coco",
        "genre": "Animation",
        "mood": "Happy",
        "rating": 8.4,
        "overview": "A beautiful and heartwarming family adventure."
    },
    {
        "title": "Jumanji",
        "genre": "Adventure",
        "mood": "Exciting",
        "rating": 7.0,
        "overview": "A fun and exciting adventure inside a magical game."
    }
]

positive_words = [
    "amazing", "wonderful", "beautiful",
    "fun", "exciting", "fascinating",
    "heartwarming", "thrilling"
]

negative_words = [
    "sad", "boring", "terrible",
    "dangerous", "bad", "scary"
]

def analyze_sentiment(text):
    words = text.lower().replace(".", "").split()
    score = 0

    for word in words:
        if word in positive_words:
            score += 1
        if word in negative_words:
            score -= 1

    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    return "Neutral"

def display_movie(movie):
    print("\n" + "=" * 40)
    print("MOVIE RECOMMENDATION")
    print("=" * 40)
    print("Title:", movie["title"])
    print("Genre:", movie["genre"])
    print("Mood:", movie["mood"])
    print("IMDb Rating:", movie["rating"])
    print("Overview:", movie["overview"])
    print("Sentiment:", analyze_sentiment(movie["overview"]))
    print("=" * 40)

def recommend():
    print("\n1 - Random movie")
    print("2 - Recommend by genre")
    print("3 - Recommend by mood")
    print("4 - Recommend by IMDb rating")
    print("5 - Exit")

    choice = input("Choose an option: ")

    if choice == "5":
        return False

    results = movies

    if choice == "2":
        genre = input("Enter genre: ").strip().lower()
        results = [
            m for m in movies
            if m["genre"].lower() == genre
        ]

    elif choice == "3":
        mood = input("Enter mood: ").strip().lower()
        results = [
            m for m in movies
            if m["mood"].lower() == mood
        ]

    elif choice == "4":
        try:
            rating = float(input("Minimum IMDb rating: "))
        except ValueError:
            print("Please enter a valid number.")
            return True

        results = [
            m for m in movies
            if m["rating"] >= rating
        ]

    elif choice != "1":
        print("Invalid option.")
        return True

    if results:
        display_movie(random.choice(results))
    else:
        print("No matching movies found.")

    return True

print("AI MOVIE RECOMMENDATION SYSTEM")

while recommend():
    pass

print("Goodbye!")
