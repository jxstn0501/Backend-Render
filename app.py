from flask import Flask, request, jsonify
import requests
import os
import tempfile

app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract():
    # API URL
    api_url = "https://api.parseextract.com/v1/data-extract"

    # Authorization
    api_key = os.environ["PARSEEXTRACT_API_KEY"]  # <<--- hier API-Key als Umgebungsvariable setzen
    headers = {"Authorization": f"Bearer {api_key}"}

    # Prompt aus dem Request holen
    prompt = request.form.get("prompt", "Extract text")
    url_param = request.form.get("url")

    # Datei speichern, falls vorhanden
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        return jsonify({"error": "No file uploaded"}), 400

    # Temporäre Datei
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        file_path = tmp.name
        uploaded_file.save(file_path)

    # Timeouts
    timeout = (10, 120)  # 10 Sekunden connect, 120 Sekunden read

    # Payload
    payload = {"prompt": prompt}
    if url_param:
        payload["url"] = url_param

    # POST Request (Sync) – exakt wie in der Dokumentation
    with open(file_path, "rb") as f:
        files = {"file": (uploaded_file.filename, f)}
        response = requests.post(api_url, files=files, data=payload, headers=headers, timeout=timeout)

    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)