import torch
from ultralytics.nn.tasks import DetectionModel
from safetensors.torch import load_file
import os

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Use relative paths from the script location
safetensor_path = os.path.join(current_dir, "icon_detect_v1_5", "model.safetensors")
output_path = os.path.join(current_dir, "icon_detect_v1_5", "model.pt")

# Verify file exists
if not os.path.exists(safetensor_path):
    raise FileNotFoundError(f"Safetensor file not found at: {safetensor_path}")

tensor_dict = load_file(safetensor_path)

# Updated by Mukesh Kumar
#model = DetectionModel(os.path.join(current_dir, "icon_detect", "model.yaml"))
model = DetectionModel(os.path.join(current_dir, "icon_detect_v1_5", "model.yaml"))
model.load_state_dict(tensor_dict)
torch.save({'model':model}, output_path)
