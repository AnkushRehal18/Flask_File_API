# app.py
from flask import Flask, request, jsonify, send_file, after_this_request
from utils.wordToPdf import convert_word_to_pdf
from utils.clearUploadFolder import clearUploadFolder
import threading
import time

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask is working! 🚀"

@app.route('/wordToPdf', methods=['POST'])
def convertToPdf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    
    pdf_path = convert_word_to_pdf(file)

    threading.Thread(target=clearUploadFolder, daemon=True).start()

    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
