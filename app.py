from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from flask import Flask, render_template, request
import json

# Create and name your chatbot
chatbot = ChatBot(
    'MyChatBot',
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    logic_adapters=[
        'chatterbot.logic.BestMatch'
    ]
)

# Train your chatbot with a predefined corpus
corpus_trainer = ChatterBotCorpusTrainer(chatbot)
corpus_trainer.train("chatterbot.corpus.english")

# Train your chatbot with custom data from a file
list_trainer = ListTrainer(chatbot)
with open('custom_conversations.json', 'r') as file:
    custom_conversations = json.load(file)
    for conversation in custom_conversations:
        list_trainer.train(conversation)

# Flask web application setup
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))

if __name__ == "__main__":
    app.run(debug=True)
