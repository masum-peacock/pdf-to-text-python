import os
import fitz  # PyMuPDF
from flask_cors import CORS  # Import CORS
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_pdf_data(file_path):
    """
    Extracts text from a PDF file at the given file path and returns it as a string.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The extracted text from the PDF file.
    """
    extracted_text = ""
    with fitz.open(file_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            extracted_text += page.get_text("text")  # Extract text from page
            extracted_text += "\n\n"  # Add spacing between pages
    return extracted_text


# default routes
@app.route("/")
def index():
    """ 
    Default route of the application, just for testing purposes.

    Returns:
        str: Hello World!
    """
    return "Hello World!"

@app.route('/upload', methods=['POST'])
def upload_pdf():
    """
    Upload a PDF file and extract text from it, saving the extracted text to a file and 
    returning it as a file download response.

    Returns:
        flask.Response: The extracted text as a file download response.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Extract data from PDF
    extracted_text = extract_pdf_data(file_path)
    
    # Save extracted text to a file
    output_file_path = os.path.join(UPLOAD_FOLDER, 'extracted_text.txt')
    with open(output_file_path, 'w', encoding='utf-8') as text_file:
        text_file.write(extracted_text)
    
    return send_file(output_file_path, as_attachment=True)

# run server
if __name__ == "__main__":
    app.run(port=8000, debug=True)