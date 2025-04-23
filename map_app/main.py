import cv2
import os
from ultralytics import YOLO
import cvzone
import psycopg2
import random

DB_CONFIG = {
    "host": "localhost",
    "user": "elcan",
    "password": "yourpassword",
    "dbname": "banner_db",
    "port": 5432
}

def save_to_database(video_id, latitude, longitude, image_link):
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        INSERT INTO locations (video_id, latitude, longitude, image_link)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (str(video_id), latitude, longitude, image_link))
        conn.commit()

        print(f"Saved to database: {image_link}")

    except psycopg2.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def detect_banners(video_path):
    model = YOLO("best-341-1600x896.pt")
    names = model.names

    cap = cv2.VideoCapture(video_path)
    width, height = 1600, 896

    best_frames = {}

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (width, height))
        results = model.track(frame, persist=True)

        if results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.int().cpu().tolist()
            class_ids = results[0].boxes.cls.int().cpu().tolist()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            confidences = results[0].boxes.conf.cpu().tolist()

            for box, class_id, track_id, conf in zip(boxes, class_ids, track_ids, confidences):
                c = names[class_id]
                x1, y1, x2, y2 = box
                area = (x2 - x1) * (y2 - y1)

                if track_id not in best_frames or area > best_frames[track_id]["area"]:
                    best_frames[track_id] = {
                        "frame": frame.copy(),
                        "box": (x1, y1, x2, y2),
                        "area": area
                    }

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cvzone.putTextRect(frame, f'{c}', (x1, y1 - 10), 1, 1)

        # Show frame in real-time
        cv2.imshow("Detection Process", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    output_dir = "static/detected_banners"
    os.makedirs(output_dir, exist_ok=True)

    for track_id, data in best_frames.items():
        x1, y1, x2, y2 = data["box"]
        latitude = round(random.uniform(40.3700, 40.4400), 6)
        longitude = round(random.uniform(49.8000, 49.9000), 6)
        banner_crop = data["frame"][y1:y2, x1:x2]
        image_link = f"{output_dir}/banner_{track_id}_best.jpg"
        cv2.imwrite(image_link, banner_crop)
        save_to_database(os.path.basename(video_path), latitude, longitude, image_link)

    return "done"

