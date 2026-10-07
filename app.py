from flask import Flask, render_template, request, jsonify

from chatbot import Chatbot


app = Flask(__name__)

# Load chatbot engine
chatbot = Chatbot("intents.json")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data.get("message", "").strip()

    result = chatbot.get_response(user_message)

    return jsonify(result)


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )