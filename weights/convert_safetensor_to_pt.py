import torch
from ultralytics.nn.tasks import DetectionModel
from safetensors.torch import load_file
import os

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Use relative paths from the script location
safetensor_path = os.path.join(current_dir, "icon_detect", "model.safetensors")
output_path = os.path.join(current_dir, "icon_detect", "model.pt")

# Verify file exists
if not os.path.exists(safetensor_path):
    raise FileNotFoundError(f"Safetensor file not found at: {safetensor_path}")

tensor_dict = load_file(safetensor_path)

model = DetectionModel(os.path.join(current_dir, "icon_detect", "model.yaml"))
model.load_state_dict(tensor_dict)
torch.save({'model':model}, output_path)
