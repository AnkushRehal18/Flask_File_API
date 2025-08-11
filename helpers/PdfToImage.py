import os
import fitz  # PyMuPDF
from flask import jsonify
from werkzeug.utils import secure_filename
import uuid

def PdfToImage(file, upload_folder="uploads"):
    if file.filename == "":
        return jsonify({"error": "Empty file name"}), 400
    
    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only .pdf files are allowed"}), 400
    
    # Use /tmp for temp storage in production
    # if upload_folder is None:
    #     upload_folder = os.path.join(tempfile.gettempdir(), "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    # Save uploaded PDF
    filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    input_path = os.path.join(upload_folder, filename)
    file.save(input_path)

    # Open PDF
    doc = fitz.open(input_path)
    image_paths = []

    try:
        for page_num in range(len(doc)):
            page = doc[page_num]
            pix = page.get_pixmap(dpi=300)
            img_filename = f"{os.path.splitext(filename)[0]}_page_{page_num + 1}.png"
            img_path = os.path.join(upload_folder, img_filename)
            pix.save(img_path)
            image_paths.append(img_path)
    except Exception as e:
        return jsonify({"error": f"An error occurred while converting PDF to images: {str(e)}"}), 500
    finally:
        doc.close()

    return image_paths
