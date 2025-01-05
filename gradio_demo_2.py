import gradio as gr
import torch
from PIL import Image
import io
from utils import check_ocr_box, get_yolo_model, get_caption_model_processor, get_som_labeled_img

# Set device to CPU only
DEVICE = torch.device('cpu')

# Load models once and cache them
model_path = 'weights/icon_detect_v1_5/model.pt'
yolo_model = get_yolo_model(model_path=model_path)
caption_model_processor = get_caption_model_processor(model_name="florence2", model_name_or_path="weights/icon_caption_florence")

def process_image(image_input, box_threshold, iou_threshold, use_paddleocr, imgsz):
    image_save_path = 'imgs/saved_image_demo.png'
    image_input.save(image_save_path)
    text, ocr_bbox = check_ocr_box(image_save_path, display_img=False, output_bb_format='xyxy', use_paddleocr=use_paddleocr)
    _, _, parsed_content_list = get_som_labeled_img(
        image_save_path, yolo_model, BOX_TRESHOLD=box_threshold, output_coord_in_ratio=True, ocr_bbox=ocr_bbox, caption_model_processor=caption_model_processor, imgsz=imgsz
    )
    parsed_content = '\n'.join(parsed_content_list)
    return parsed_content

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Image to Parsed Screen Elements")
    with gr.Row():
        image_input = gr.Image(type="pil", label="Upload Image")
        box_threshold = gr.Slider(label="Box Threshold", minimum=0.01, maximum=1.0, step=0.01, value=0.05)
        iou_threshold = gr.Slider(label="IOU Threshold", minimum=0.01, maximum=1.0, step=0.01, value=0.1)
        use_paddleocr = gr.Checkbox(label="Use PaddleOCR", value=True)
        imgsz = gr.Slider(label="Image Size", minimum=640, maximum=1920, step=32, value=640)
        text_output = gr.Textbox(label="Parsed Screen Elements")
    
    submit_button = gr.Button("Process Image")
    submit_button.click(
        fn=process_image,
        inputs=[image_input, box_threshold, iou_threshold, use_paddleocr, imgsz],
        outputs=[text_output]
    )

# Launch the Gradio app
demo.launch(server_name="0.0.0.0", server_port=58080)
