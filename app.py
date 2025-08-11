from flask import Flask, request, jsonify, send_file, after_this_request
from helpers.wordToPdf import convert_word_to_pdf
from utils.clearUploadFolder import clearUploadFolder
from helpers.PdfToWord import convert_pdf_to_word
from helpers.imageToPdf import imageToPdf
from helpers.PdfToImage import PdfToImage
import threading
import os
import zipfile
import io
app = Flask(__name__)

@app.route('/wordToPdf', methods=['POST'])
def convertToPdf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    
    pdf_path = convert_word_to_pdf(file)

    threading.Thread(target=clearUploadFolder, daemon=True).start()

    return send_file(pdf_path, as_attachment=True)


@app.route('/pdfToWord', methods=['POST'])

def convertToWord():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    
    try:
        word_path = convert_pdf_to_word(file)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except RuntimeError as re:
        return jsonify({"error": str(re)}), 500
    
    # print(word_path)
    threading.Thread(target=clearUploadFolder, daemon=True).start()

    return send_file(
        word_path,
        as_attachment=True,
        download_name=os.path.basename(word_path),
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )


@app.route("/jpgToPdf", methods=["POST"])

def jpgToPdf():
    if "image_key" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    image_file = request.files["image_key"]
    try:
        pdf_path = imageToPdf(image_file)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # message= "Image converted to PDF successfully."
    threading.Thread(target=clearUploadFolder, daemon=True).start()

    return send_file(pdf_path, as_attachment=True  )

@app.route("/pdftoimage", methods=["POST"])
def pdf_to_image_route():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]

    try:
        image_paths = PdfToImage(file)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Create a ZIP in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for img_path in image_paths:
            zipf.write(img_path, os.path.basename(img_path))
    zip_buffer.seek(0)

    return send_file(zip_buffer, as_attachment=True, download_name="pdf_images.zip", mimetype="application/zip")

if __name__ == "__main__":
    app.run(debug=True)
