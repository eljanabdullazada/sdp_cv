from ultralytics import YOLO

# Load a COCO-pretrained YOLO11n model
# model = YOLO("yolo11n.pt")  # Detection
model = YOLO("yolo11x-seg.pt")  # Instance Segmentation

# Run inference with the YOLO11n model on the 'bus.jpg' image
results = model("input/240.png", save=True, show=True)