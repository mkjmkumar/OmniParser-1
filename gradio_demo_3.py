import gradio as gr
import torch
from PIL import Image
import io
from utils import check_ocr_box, get_yolo_model, get_caption_model_processor, get_som_labeled_img
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read values from .env
BOX_THRESHOLD = float(os.getenv("BOX_THRESHOLD", 0.05))
IOU_THRESHOLD = float(os.getenv("IOU_THRESHOLD", 0.1))
USE_PADDLEOCR = os.getenv("USE_PADDLEOCR", "True").lower() == "true"
IMGSZ = int(os.getenv("IMGSZ", 640))

# Set device to CPU only
DEVICE = torch.device('cpu')

# Load models once and cache them
model_path = 'weights/icon_detect_v1_5/model.pt'
yolo_model = get_yolo_model(model_path=model_path)
caption_model_processor = get_caption_model_processor(model_name="florence2", model_name_or_path="weights/icon_caption_florence")

def process_image(image_input):
    image_save_path = 'imgs/saved_image_demo.png'
    image_input.save(image_save_path)
    text, ocr_bbox = check_ocr_box(image_save_path, display_img=False, output_bb_format='xyxy', use_paddleocr=USE_PADDLEOCR)
    _, _, parsed_content_list = get_som_labeled_img(
        image_save_path, yolo_model, BOX_TRESHOLD=BOX_THRESHOLD, output_coord_in_ratio=True, ocr_bbox=ocr_bbox, caption_model_processor=caption_model_processor, imgsz=IMGSZ
    )
    parsed_content = '\n'.join(parsed_content_list)
    return parsed_content

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Image to Parsed Screen Elements")
    with gr.Row():
        image_input = gr.Image(type="pil", label="Upload Image")
        text_output = gr.Textbox(label="Parsed Screen Elements")
    submit_button = gr.Button("Process Image")
    submit_button.click(fn=process_image, inputs=[image_input], outputs=[text_output])

# Launch the Gradio app
demo.launch(server_name="0.0.0.0", server_port=58080)
