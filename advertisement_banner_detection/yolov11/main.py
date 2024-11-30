from ultralytics import YOLO

# Load a COCO-pretrained YOLO11n model
# model = YOLO("yolo11n.pt")  # Detection
# model = YOLO("yolo11x-seg.pt")  # Instance Segmentation
# model = YOLO("yolo11x-obb.pt")  # Oriented Bounding Boxes Object Detection
# model = YOLO("yolo11x-cls.pt")  # Image Classification

# Run inference with the YOLO11n model on the 'bus.jpg' image
results = model("input/258.png", save=True, show=True)