import cv2
import os
import numpy as np

# Paths
video_path = r"C:\Users\user\Downloads\sdp_cv\advertisement_banner_detection\data\videos\dashcam_video.mp4"
frames_folder = r"C:\Users\user\Downloads\sdp_cv\advertisement_banner_detection\data\frames"

# Ensure the frames folder exists
os.makedirs(frames_folder, exist_ok=True)

def process_video_and_detect_lines(video_path, frames_folder, max_frames=180, skip_frames=60):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    saved_frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or saved_frame_count >= max_frames:
            break

        # Process only every `skip_frames` frame
        if frame_count % skip_frames == 0:
            processed_frame = detect_lines_on_frame(frame)
            frame_filename = os.path.join(frames_folder, f"frame_{saved_frame_count:04d}.jpg")
            cv2.imwrite(frame_filename, processed_frame)
            saved_frame_count += 1
            print(f"Processed and saved frame: {frame_filename}")

        frame_count += 1

    cap.release()

def detect_lines_on_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Get frame dimensions
    height, width = edges.shape

    # Crop the top-right corner (adjust the dimensions as necessary)
    cropped_edges = edges[0:int(height/2), int(width/2):width]

    # Detect lines using Hough Transform
    lines = cv2.HoughLinesP(cropped_edges, rho=1, theta=np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1 + int(width / 2), y1), (x2 + int(width / 2), y2), (0, 255, 0), 2)

    return frame

# Execute the processing
process_video_and_detect_lines(video_path, frames_folder, max_frames=180, skip_frames=60)
