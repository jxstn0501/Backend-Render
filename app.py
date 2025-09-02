from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_URL = "https://api.parseextract.com/v1/data-extract"
API_KEY = os.environ.get("PARSEEXTRACT_API_KEY")

@app.route("/extract", methods=["POST"])
def extract():
    file = request.files.get("file")
    prompt = request.form.get("prompt", "")

    if not file or not prompt:
        return jsonify({"error": "file and prompt are required"}), 400

    headers = {"Authorization": f"Bearer {API_KEY}"}
    files = {"file": (file.filename, file.stream, file.mimetype)}
    data = {"prompt": prompt}

    try:
        resp = requests.post(API_URL, files=files, data=data, headers=headers, timeout=(10,120))
        return jsonify(resp.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Backend läuft! Sende POST an /extract"