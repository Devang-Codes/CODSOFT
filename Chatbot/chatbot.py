import datetime
import random

print("=" * 50)
print("🤖 Welcome to CodSoft AI Chatbot")
print("Type 'exit' to end the conversation.")
print("=" * 50)

greetings = [
    "Hello! How can I help you?",
    "Hi there! Nice to meet you.",
    "Hey! What can I do for you today?"
]

while True:
    user_input = input("\nYou: ").lower().strip()

    # Exit
    if user_input in ["exit", "quit", "bye"]:
        print("Bot: Goodbye! Have a great day 😊")
        break

    # Greetings
    elif any(word in user_input for word in ["hello", "hi", "hey"]):
        print("Bot:", random.choice(greetings))

    # Name
    elif "your name" in user_input:
        print("Bot: I am CodSoft AI Chatbot.")

    # Time
    elif "time" in user_input:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"Bot: Current time is {current_time}")

    # Date
    elif "date" in user_input:
        current_date = datetime.datetime.now().strftime("%d-%m-%Y")
        print(f"Bot: Today's date is {current_date}")

    # AI
    elif "artificial intelligence" in user_input or "ai" in user_input:
        print("Bot: AI is the simulation of human intelligence in machines.")

    # Machine Learning
    elif "machine learning" in user_input:
        print("Bot: Machine Learning is a subset of AI that learns from data.")

    # Python
    elif "python" in user_input:
        print("Bot: Python is one of the most popular programming languages for AI.")

    # Internship
    elif "internship" in user_input:
        print("Bot: Internships help students gain practical experience.")

    # Help
    elif "help" in user_input:
        print("Bot: You can ask me about AI, Python, date, time, or internships.")

    # Thanks
    elif "thank" in user_input:
        print("Bot: You're welcome! 😊")

    # Default response
    else:
        print("Bot: Sorry, I don't understand that. Try asking something else.")