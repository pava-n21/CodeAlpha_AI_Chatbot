import json
import random
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Chatbot:

    def __init__(self, data_file):

        # Load knowledge base
        with open(data_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.intents = data["intents"]

        self.patterns = []
        self.tags = []

        # Prepare chatbot patterns
        for intent in self.intents:

            if intent["tag"] == "fallback":
                continue

            for pattern in intent["patterns"]:

                self.patterns.append(pattern)
                self.tags.append(intent["tag"])

        # TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )

        self.pattern_vectors = self.vectorizer.fit_transform(
            self.patterns
        )

    def tokenize(self, text):
        """
        Convert text into meaningful lowercase words.
        """

        words = re.findall(
            r"\b[a-zA-Z]+\b",
            text.lower()
        )

        # Common words that don't help identify intent
        stop_words = {
            "a", "an", "the",
            "is", "are", "was", "were",
            "am", "be", "been",
            "do", "does", "did",
            "i", "me", "my",
            "you", "your",
            "we", "our",
            "they", "their",
            "it", "its",
            "to", "for", "of",
            "on", "in", "at",
            "from", "with",
            "can", "could",
            "would", "should",
            "please",
            "what", "how",
            "where", "when",
            "who", "why",
            "tell"
        }

        return {
            word
            for word in words
            if word not in stop_words
        }

    def get_fallback_response(self, confidence=0.0):

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

    def get_response(self, user_message):

        user_message = user_message.strip()

        # -----------------------------------------
        # EMPTY MESSAGE
        # -----------------------------------------

        if not user_message:

            return {
                "response": "Please enter a message.",
                "intent": "empty",
                "confidence": 0.0
            }

        # -----------------------------------------
        # CONVERT USER MESSAGE TO TF-IDF
        # -----------------------------------------

        user_vector = self.vectorizer.transform(
            [user_message]
        )

        # -----------------------------------------
        # CALCULATE COSINE SIMILARITY
        # -----------------------------------------

        similarity_scores = cosine_similarity(
            user_vector,
            self.pattern_vectors
        )[0]

        # -----------------------------------------
        # BEST MATCH
        # -----------------------------------------

        best_match_index = similarity_scores.argmax()

        confidence = float(
            similarity_scores[best_match_index]
        )

        # Matched pattern
        matched_pattern = self.patterns[
            best_match_index
        ]

        # Matched intent
        matched_tag = self.tags[
            best_match_index
        ]

        # -----------------------------------------
        # ACCURACY CHECK 1
        # -----------------------------------------

        # Reject weak matches.

        if confidence < 0.35:

            return self.get_fallback_response(
                confidence
            )

        # -----------------------------------------
        # ACCURACY CHECK 2
        # -----------------------------------------

        # Compare meaningful words.

        user_words = self.tokenize(
            user_message
        )

        pattern_words = self.tokenize(
            matched_pattern
        )

        common_words = user_words.intersection(
            pattern_words
        )

        # -----------------------------------------
        # ACCURACY CHECK 3
        # -----------------------------------------

        # If the user has meaningful words but
        # none of them exist in the matched
        # pattern, reject the match.

        if len(user_words) >= 2:

            if len(common_words) == 0:

                return self.get_fallback_response(
                    confidence
                )

        # -----------------------------------------
        # ACCURACY CHECK 4
        # -----------------------------------------

        # For longer questions, require at least
        # one meaningful matching word.

        if len(user_words) >= 3:

            if len(common_words) < 1:

                return self.get_fallback_response(
                    confidence
                )

        # -----------------------------------------
        # RETURN MATCHED RESPONSE
        # -----------------------------------------

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


# =============================================
# TERMINAL TEST
# =============================================

if __name__ == "__main__":

    chatbot = Chatbot("intents.json")

    print()
    print("===================================")
    print("          AI CHATBOT ENGINE")
    print("===================================")
    print("Type 'exit' to stop.")
    print()

    while True:

        user_message = input("You: ")

        if user_message.lower().strip() == "exit":

            print("Chatbot: Goodbye!")
            break

        result = chatbot.get_response(
            user_message
        )

        print(
            "Chatbot:",
            result["response"]
        )

        print(
            "Intent:",
            result["intent"],
            "| Confidence:",
            round(
                result["confidence"],
                2
            )
        )

        print()