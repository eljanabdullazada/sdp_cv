import os
import subprocess
from roboflow import Roboflow
# Get current script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(SCRIPT_DIR, "datasets")
os.makedirs(DATASET_DIR, exist_ok=True)

# Run YOLOv11 training
subprocess.run([
    "yolo", "task=detect", "mode=train",
    "model=yolo11n.pt",
    f"data={DATASET_DIR}/Advertisement-Banners-3-2/data.yaml",
    "epochs=100", "imgsz=1600,896", "plots=True"
], check=True)