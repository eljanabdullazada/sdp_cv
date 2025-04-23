import cv2
import os
import random
import cvzone
from ultralytics import YOLO
from db import insert_banner_data
from models import Location, db
from flask import current_app

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
    width, height = 1600, 896
    best_frames = {}
    video_name = os.path.basename(video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (width, height))
        results = model.predict(frame, verbose=False)

        if results[0].boxes and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.int().cpu().tolist()
            class_ids = results[0].boxes.cls.int().cpu().tolist()
            track_ids = results[0].boxes.id.int().cpu().tolist() if results[0].boxes.id is not None else [0] * len(boxes)
            confidences = results[0].boxes.conf.cpu().tolist()

            for box, class_id, track_id, conf in zip(boxes, class_ids, track_ids, confidences):
                x1, y1, x2, y2 = box
                area = (x2 - x1) * (y2 - y1)

                if track_id not in best_frames or area > best_frames[track_id]["area"]:
                    best_frames[track_id] = {
                        "frame": frame.copy(),
                        "box": (x1, y1, x2, y2),
                        "area": area
                    }

    cap.release()

    for track_id, data in best_frames.items():
        x1, y1, x2, y2 = data["box"]
        banner_crop = data["frame"][y1:y2, x1:x2]
        image_path = f"{output_dir}/banner_{track_id}_best.jpg"
        cv2.imwrite(image_path, banner_crop)

        lat = round(random.uniform(40.3700, 40.4400), 6)
        lon = round(random.uniform(49.8000, 49.9000), 6)
        save_to_database(video_id=video_name, latitude=lat, longitude=lon, image_path=image_path)

    return "done"



def generate_stream(filename):
    cap = cv2.VideoCapture(os.path.join("videos", filename))
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.resize(frame, (1600, 896))
        results = model.track(frame, persist=True)

        if results[0].boxes and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.int().cpu().tolist()
            class_ids = results[0].boxes.cls.int().cpu().tolist()
            track_ids = results[0].boxes.id.int().cpu().tolist()

            for box, class_id, track_id in zip(boxes, class_ids, track_ids):
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
