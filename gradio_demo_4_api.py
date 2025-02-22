from flask import Flask, request, jsonify
import torch
from PIL import Image
from io import BytesIO
from utils import check_ocr_box, get_yolo_model, get_caption_model_processor, get_som_labeled_img
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Read values from .env
BOX_THRESHOLD = float(os.getenv("BOX_THRESHOLD", 0.05))
IOU_THRESHOLD = float(os.getenv("IOU_THRESHOLD", 0.1))
USE_PADDLEOCR = os.getenv("USE_PADDLEOCR", "True").lower() == "true"
IMGSZ = int(os.getenv("IMGSZ", 640))

# Initialize Flask app
app = Flask(__name__)

# Load models once
model_path = 'weights/icon_detect_v1_5/model.pt'
yolo_model = get_yolo_model(model_path=model_path)
caption_model_processor = get_caption_model_processor(model_name="florence2", model_name_or_path="weights/icon_caption_florence")

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        image = Image.open(file.stream)

        # Save the image temporarily
        temp_image_path = '/opt/app-root/src/OmniParser/imgs/temp_image.png'
        image.save(temp_image_path)

        # Process the image
        text, ocr_bbox = check_ocr_box(
            temp_image_path, display_img=False, output_bb_format='xyxy', use_paddleocr=USE_PADDLEOCR
        )
        _, _, parsed_content_list = get_som_labeled_img(
            temp_image_path,
            yolo_model,
            BOX_TRESHOLD=BOX_THRESHOLD,  # ensure the parameter name is correct
            output_coord_in_ratio=True,
            ocr_bbox=ocr_bbox,
            caption_model_processor=caption_model_processor,
            imgsz=IMGSZ
        )

        parsed_content = '\n'.join(parsed_content_list)
        return jsonify({'parsed_content': parsed_content})
    except Exception as e:
        # Log the error to the console and return it in JSON format
        print("Error processing image:", e)
        return jsonify({'error': str(e)}), 500


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=58085)
