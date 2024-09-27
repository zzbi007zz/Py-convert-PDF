from flask import Flask, request, jsonify
import PyPDF2
import os
import logging

# Initialize the Flask application
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/upload', methods=['POST'])
def upload():
    logging.debug("Received request to upload file")
    
    # Check if a file is part of the request
    if 'file' not in request.files:
        logging.error('No file part in the request')
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # Check if the file has a filename
    if file.filename == '':
        logging.error('No selected file')
        return jsonify({'error': 'No selected file'}), 400

    # Save the file to a temporary directory
    file_path = os.path.join('/tmp', file.filename)
    logging.debug("Saving file to: %s", file_path)
    file.save(file_path)

    # Convert the PDF to text
    text = convert_pdf_to_text(file_path)

    # Optionally delete the file after processing
    os.remove(file_path)
    logging.debug("Deleted the temporary file: %s", file_path)

    # Return the extracted text
    return jsonify({'text': text}), 200

def convert_pdf_to_text(pdf_path):
    """Convert PDF file to text."""
    text = ''
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + '\\n'
    return text

if __name__ == '__main__':
    app.run(debug=True)