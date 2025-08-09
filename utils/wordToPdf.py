import os
from docx2pdf import convert
from werkzeug.utils import secure_filename
from flask import jsonify

def convert_word_to_pdf(uploaded_file, upload_folder="uploads"):
    if uploaded_file.filename == "":
        return jsonify({"error": "Empty File name"}), 400
    
    if not uploaded_file.filename.endswith(".docx"):
        return jsonify({"error": "Only .docx files are allowed"}), 400
    
    # Ensure upload folder exists
    os.makedirs(upload_folder, exist_ok=True)

    # Save uploaded file temporarily
    filename = secure_filename(uploaded_file.filename)
    input_path = os.path.join(upload_folder, filename)
    uploaded_file.save(input_path)

    # Create output file path
    output_path = os.path.splitext(input_path)[0] + ".pdf"

    # Convert Word to PDF
    convert(input_path, output_path)

    return output_path  # This will be sent back by Flask route


