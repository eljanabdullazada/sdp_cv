import os
import subprocess

# Get current script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(SCRIPT_DIR, "datasets")
os.makedirs(DATASET_DIR, exist_ok=True)

# Change to dataset directory
os.chdir(DATASET_DIR)

# Install required dependencies
subprocess.run(["pip", "install", "roboflow", "ultralytics", "--quiet"], check=True)

# Change back to script directory
os.chdir(SCRIPT_DIR)

# Run YOLOv11 training
subprocess.run([
    "yolo", "task=detect", "mode=train",
    "model=yolo11n.pt",
    f"data={DATASET_DIR}/Advertisement-Banners-3-2/data.yaml",
    "epochs=100", "imgsz=640", "plots=True"
], check=True)