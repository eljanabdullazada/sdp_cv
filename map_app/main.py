import cv2
import os
import random
import cvzone
from ultralytics import YOLO
from db import insert_banner_data
from models import Location, db
from flask import current_app
import re

import pytesseract

model = YOLO("best-341-1600x896.pt")
names = model.names
output_dir = "static/detected_banners"
os.makedirs(output_dir, exist_ok=True)

stop_detection = False


def save_to_database(video_id, latitude, longitude, image_path):
    location = Location(
        video_name=str(video_id),
        latitude=latitude,
        longitude=longitude,
        image_path=image_path
    )
    db.session.add(location)
    db.session.commit()
    print(f"[DB] Saved: {image_path}")



def detect_banners(video_path):
    cap = cv2.VideoCapture(video_path)
    width, height = 1280, 736
    best_frames = {}
    video_name = os.path.basename(video_path)

    print("| Detection has started |")
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (width, height))
        results = model.predict(frame, verbose=False)

        if results and results[0].boxes:
            boxes = results[0].boxes.xyxy.int().cpu().tolist()
            class_ids = results[0].boxes.cls.int().cpu().tolist()
            confidences = results[0].boxes.conf.cpu().tolist()
            track_ids = list(range(len(boxes)))  # Fallback: use index as ID

            for box, class_id, track_id, conf in zip(boxes, class_ids, track_ids, confidences):
                x1, y1, x2, y2 = box
                width_box = x2 - x1
                height_box = y2 - y1
                area = width_box * height_box

                if width_box > height_box:  # only consider wide rectangles
                    if track_id not in best_frames or area > best_frames[track_id]["area"]:
                        best_frames[track_id] = {
                            "frame": frame.copy(),
                            "box": (x1, y1, x2, y2),
                            "area": area,
                            "frame_id": frame_idx
                        }

        frame_idx += 1

    cap.release()

    print("\n[INFO] Performing OCR and saving best frames...")

    for track_id, data in best_frames.items():
        x1, y1, x2, y2 = data["box"]
        frame2 = data["frame"]

        # OCR section (bottom-right GPS detection)
        frame_h, frame_w = frame2.shape[:2]
        gps_y1 = int(frame_h * 0.75)
        gps_x1 = int(frame_w * 0.5)
        gps_region = frame2[gps_y1:frame_h, gps_x1:frame_w]

        gps_gray = cv2.cvtColor(gps_region, cv2.COLOR_BGR2GRAY)
        _, gps_thresh = cv2.threshold(gps_gray, 150, 255, cv2.THRESH_BINARY)

        text = pytesseract.image_to_string(gps_thresh).strip()
        gps_pattern = r"(\d{2,3}\.\d{6,8})([NS])\s+(\d{2,3}\.\d{6,8})([EW])"
        match = re.search(gps_pattern, text)

        latitude = longitude = None
        if match:
            lat_val = float(match.group(1))
            lat_dir = match.group(2)
            lon_val = float(match.group(3))
            lon_dir = match.group(4)
            latitude = -lat_val if lat_dir == 'S' else lat_val
            longitude = -lon_val if lon_dir == 'W' else lon_val

        # Save banner crop
        banner_crop = frame2[y1:y2, x1:x2]
        image_path = f"{output_dir}/banner_{track_id}_best.jpg"
        cv2.imwrite(image_path, banner_crop)

        # Save to DB
        if latitude is not None and longitude is not None:
            save_to_database(video_name, latitude, longitude, image_path)
        else:
            print(f"[WARN] GPS not found for track_id={track_id}, image={image_path}")





def generate_stream(filename):
    cap = cv2.VideoCapture(os.path.join("videos", filename))
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.resize(frame, (1600, 896))
        results = model.predict(frame, verbose=False)

        if results and results[0].boxes:
            boxes = results[0].boxes.xyxy.int().cpu().tolist()
            class_ids = results[0].boxes.cls.int().cpu().tolist()

            for box, class_id in zip(boxes, class_ids):
                x1, y1, x2, y2 = box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cvzone.putTextRect(frame, f'{names[class_id]}', (x1, y1 - 10), 1, 1)

        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    cap.release()



def stop_live_detection():
    global stop_detection
    stop_detection = True
