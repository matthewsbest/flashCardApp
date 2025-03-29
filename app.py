from flask import Flask, render_template, jsonify, request
import random
import json

app = Flask(__name__)

# Load words from JSON
with open("words.json", "r") as f:
    word_data = json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_words", methods=["POST"])
def get_words():
    level = request.json.get("level")
    words = word_data.get(level, [])
    random.shuffle(words)
    
    return jsonify({
        "words": words,
        "total_words": sum(len(v) for v in word_data.values())
    })

if __name__ == "__main__":
    app.run(debug=True)
