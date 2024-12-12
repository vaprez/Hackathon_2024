from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Remplacez ces valeurs par vos propres valeurs
HOST = "your-host-url"
API_KEY = "your-api-key"

@app.route("/", methods=["GET"])
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(debug=True)
