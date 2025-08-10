import os
from pdf2docx import Converter
from werkzeug.utils import secure_filename
from flask import jsonify


def convert_pdf_to_word(file, upload_folder = "uploads"):
    if file.filename == "":
        return jsonify({"error": "Empty File name"}), 400
    
    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Only .pdf files are allowed"}), 400
    
    # Ensure upload folder exists
    os.makedirs(upload_folder, exist_ok=True)

    # Save uploaded file temporarily
    filename = secure_filename(file.filename)
    input_path = os.path.join(upload_folder, filename)
    file.save(input_path)

    # Create output file path
    output_path = os.path.splitext(input_path)[0] + ".docx"

    # Convert Word to PDF
    try:
        cv = Converter(input_path)
        cv.convert(output_path, start=0, end=None)
        cv.close()
    except Exception as e:
        raise RuntimeError(f"Conversion failed: {str(e)}")

    return output_path  # This will be sent back by Flask route