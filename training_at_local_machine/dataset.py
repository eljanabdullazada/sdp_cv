import os
import subprocess
from roboflow import Roboflow
# Get current script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(SCRIPT_DIR, "datasets")
os.makedirs(DATASET_DIR, exist_ok=True)

# Change to dataset directory
os.chdir(DATASET_DIR)

# Install required dependencies
subprocess.run(["pip", "install", "roboflow", "ultralytics", "--quiet"], check=True)

# Download dataset from Roboflow

rf = Roboflow(api_key="v2yit2AkrEi3NVeDWdMu")
project = rf.workspace("vagifs-workspace").project("advertisement-banners-3")
version = project.version(2)
dataset = version.download("yolov11")

# Change back to script directory
os.chdir(SCRIPT_DIR)