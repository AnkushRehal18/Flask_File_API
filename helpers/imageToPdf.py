from flask import jsonify
import os
from werkzeug.utils import secure_filename
from img2pdf import convert

allowed_extensions = {'jpg', 'jpeg', 'png'}

def imageToPdf(img, upload_folder = "uploads"):

    if img.filename == "":
        return jsonify({"error":"image name cannot be empty"})
    
    if not img.filename.split('.')[-1].lower() in allowed_extensions:
        return jsonify({"error": "Only .jpg, .jpeg, and .png files are allowed"}), 400
    
        # Ensure upload folder exists
    os.makedirs(upload_folder, exist_ok=True)

    # Save uploaded file temporarily
    filename = secure_filename(img.filename)
    input_path = os.path.join(upload_folder, filename)
    img.save(input_path)

    output_path = os.path.splitext(input_path)[0] + ".pdf"

    try:
        with open(input_path , "rb") as img_file:
            pdf_bytes = convert(img_file)

        with open(output_path, "wb") as pdf_file:
            pdf_file.write(pdf_bytes)

        print(f"Successfully converted image to pdf ")

    except FileNotFoundError:
        print(f"Error: The file path was not found.")

    except Exception as e:
        print(f"An error occurred: {e}")

    return output_path