import json
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Chatbot:

    def __init__(self, data_file):
        # Load chatbot knowledge base
        with open(data_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.intents = data["intents"]

        self.patterns = []
        self.tags = []

        # Prepare training patterns
        for intent in self.intents:

            # Skip fallback because it has no patterns
            if intent["tag"] == "fallback":
                continue

            for pattern in intent["patterns"]:
                self.patterns.append(pattern)
                self.tags.append(intent["tag"])

        # Convert text into TF-IDF vectors
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )

        self.pattern_vectors = self.vectorizer.fit_transform(
            self.patterns
        )

    def get_response(self, user_message):

        user_message = user_message.strip()

        # Empty message
        if not user_message:
            return {
                "response": "Please enter a message.",
                "intent": "empty",
                "confidence": 0.0
            }

        # Convert user message into TF-IDF vector
        user_vector = self.vectorizer.transform(
            [user_message]
        )

        # Calculate similarity
        similarity_scores = cosine_similarity(
            user_vector,
            self.pattern_vectors
        )[0]

        # Find best matching pattern
        best_match_index = similarity_scores.argmax()

        confidence = float(
            similarity_scores[best_match_index]
        )

        # If similarity is too low, use fallback
        if confidence < 0.20:

            fallback_intent = next(
                intent
                for intent in self.intents
                if intent["tag"] == "fallback"
            )

            return {
                "response": random.choice(
                    fallback_intent["responses"]
                ),
                "intent": "fallback",
                "confidence": confidence
            }

        # Get matched intent
        matched_tag = self.tags[best_match_index]

        matched_intent = next(
            intent
            for intent in self.intents
            if intent["tag"] == matched_tag
        )

        return {
            "response": random.choice(
                matched_intent["responses"]
            ),
            "intent": matched_tag,
            "confidence": confidence
        }


# Test chatbot from terminal
if __name__ == "__main__":

    chatbot = Chatbot("intents.json")

    print()
    print("===================================")
    print("        AI CHATBOT ENGINE")
    print("===================================")
    print("Type 'exit' to stop.")
    print()

    while True:

        user_message = input("You: ")

        if user_message.lower().strip() == "exit":
            print("Chatbot: Goodbye!")
            break

        result = chatbot.get_response(user_message)

        print("Chatbot:", result["response"])
        print(
            "Intent:",
            result["intent"],
            "| Confidence:",
            round(result["confidence"], 2)
        )
        print()