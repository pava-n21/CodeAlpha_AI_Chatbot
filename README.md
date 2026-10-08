# CodeAlpha AI Chatbot

## Project Overview

CodeAlpha AI Chatbot is a retrieval-based AI chatbot developed as part of the CodeAlpha Cloud Computing Internship.

The chatbot provides instant responses to user questions through a web-based interface. It uses Natural Language Processing techniques to identify the most relevant predefined response from a knowledge base.

## Features

- Interactive web-based chatbot
- Retrieval-based response system
- TF-IDF text vectorization
- Cosine similarity for intent matching
- Multiple predefined conversation intents
- Fallback response for unknown questions
- Flask backend
- HTML, CSS and JavaScript frontend
- AWS EC2 cloud deployment
- GitHub source-code management
- Improved response accuracy using keyword validation

## Technologies Used

- Python
- Flask
- Scikit-learn
- TF-IDF
- Cosine Similarity
- HTML5
- CSS3
- JavaScript
- AWS EC2
- Git/GitHub

## System Architecture

User
↓
Web Chatbot Interface
↓
Flask Backend
↓
Chatbot Engine
↓
TF-IDF Vectorization
↓
Cosine Similarity
↓
Intent Matching
↓
Knowledge Base
↓
Response

## Project Structure

CodeAlpha_AI_Chatbot/
│
├── venv/
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── intents.json
├── chatbot.py
├── app.py
├── requirements.txt
└── README.md

## How It Works

1. The user enters a question in the chatbot interface.
2. The request is sent to the Flask backend.
3. The chatbot converts the input into TF-IDF features.
4. Cosine similarity compares the input with predefined patterns.
5. The most relevant intent is selected.
6. The chatbot returns a predefined response.
7. If the confidence is too low or the meaningful words do not match the selected pattern, a fallback response is returned.

## Cloud Deployment

The chatbot is deployed on an AWS EC2 Ubuntu server.

The Flask application is configured to listen on:

0.0.0.0:5000

The application can therefore be accessed through the EC2 public IP address.

## Running Locally

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the application:

python app.py

Then open:

http://127.0.0.1:5000

## Internship Task

This project was developed for:

CodeAlpha Cloud Computing Internship

Task 4 – AI Chatbot

The task permits either a retrieval-based or generative chatbot approach.

## Future Enhancements

- Larger knowledge base
- More advanced NLP techniques
- Voice interaction
- Authentication
- Conversation history
- Production WSGI deployment
- Database integration
- Integration with a generative AI model