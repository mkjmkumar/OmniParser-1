from flask import Flask, request, jsonify
from flasgger import Swagger
from PIL import Image
import os
import logging
import tempfile

from dotenv import load_dotenv
load_dotenv()

# For OCR
from utils import check_ocr_box

# Environment variables
USE_PADDLEOCR = os.getenv("USE_PADDLEOCR", "True").lower() == "true"

# Initialize Flask app
app = Flask(__name__)
swagger = Swagger(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/process_image', methods=['POST'])
def process_image():
    """
    Process an uploaded image to extract OCR data using a unique temp file path.
    ---
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: file
        type: file
        required: true
        description: The image file to process.
    responses:
      200:
        description: The OCR data extracted from the image.
        schema:
          type: object
          properties:
            parsed_content:
              type: string
              description: The parsed OCR content from the image.
      400:
        description: Bad Request - No file provided.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    uploaded_file = request.files['file']
    try:
        # 1) Load the image in-memory (PIL)
        pil_image = Image.open(uploaded_file.stream)

        # 2) Create a unique temp file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            temp_path = tmp.name
            pil_image.save(tmp, format='PNG')

        try:
            # 3) Run ONLY check_ocr_box to get OCR text
            text, ocr_bbox = check_ocr_box(
                temp_path,
                display_img=False,
                output_bb_format='xyxy',
                use_paddleocr=USE_PADDLEOCR
            )

            # 'text' might be the recognized text
            # If check_ocr_box returns multiple lines, you can join them or structure them
            # For now, let's just send 'text' directly:
            return jsonify({'parsed_content': text})

        finally:
            # 4) Clean up the temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    except Exception:
        logger.exception("Error processing image")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # For local/debug only
    app.run(host='0.0.0.0', port=58090, threaded=True)
