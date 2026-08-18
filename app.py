import os

from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/app.js")
def javascript():
    return send_from_directory(".", "app.js")


@app.route("/style.css")
def stylesheet():
    return send_from_directory(".", "style.css")


@app.route("/service-worker.js")
def service_worker():
    return send_from_directory(".", "service-worker.js")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "error": "Message is required"
        }), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        return jsonify({
            "response": response.choices[0].message.content
        })

    except Exception as error:
        print("OpenAI API error:", error)

        return jsonify({
            "error": "Unable to get a response from OpenAI"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)