import cv2
import os
import numpy as np

# Paths
video_path = r"C:\Users\user\Desktop\sdp_cv-1\advertisement_banner_detection\data\videos\dashcam_video.mp4"
frames_folder = r"C:\Users\user\Desktop\sdp_cv-1\advertisement_banner_detection\data\frames"

# Ensure the frames folder exists
os.makedirs(frames_folder, exist_ok=True)

# Parameters
max_frames = 180

def process_video_and_detect_lines(video_path, frames_folder, skip_frames=1):
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Failed to open video file {video_path}")
        return

    print(f"Processing video: {video_path}")

    frame_count = 0
    saved_frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame is None or saved_frame_count >= max_frames:
            break

        # Process only every skip_frames frame
        if frame_count % skip_frames == 0:
            processed_frame = detect_lines_with_borders(frame)
            frame_filename = os.path.join(frames_folder, f"frame_{saved_frame_count:04d}.jpg")
            cv2.imwrite(frame_filename, processed_frame)
            saved_frame_count += 1
            print(f"Processed and saved into: {frame_filename}")

        frame_count += 1

    cap.release()

def detect_lines_with_borders(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Get frame dimensions
    height, width = edges.shape

    # Define the region of interest (top-right quadrant)
    roi_x_start = int(width * 0.5)  # Middle of width
    roi_x_end = width  # Full width
    roi_y_start = 0  # Top of the image
    roi_y_end = int(height * 0.5)  # Middle of height

    cropped_edges = edges[roi_y_start:roi_y_end, roi_x_start:roi_x_end]
    frame_roi = frame[roi_y_start:roi_y_end, roi_x_start:roi_x_end]

    # Detect lines using Hough Transform
    min_line_length = int(width * 0.15)  # 15% of width
    min_line_height = int(height * 0.1)  # 10% of height
    lines = cv2.HoughLinesP(cropped_edges, rho=1, theta=np.pi/180, threshold=50, minLineLength=min_line_length, maxLineGap=15)

    detected_lines = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            
            # Convert to global coordinates
            x1 += roi_x_start
            x2 += roi_x_start
            y1 += roi_y_start
            y2 += roi_y_start

            # Ensure the line meets both width and height conditions
            line_width = abs(x2 - x1)
            line_height = abs(y2 - y1)

            if line_width >= min_line_length or line_height >= min_line_height:
                detected_lines.append(((x1, y1), (x2, y2)))
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Detect borders (gray/black areas)
    detect_borders(frame, detected_lines)

    return frame

def detect_borders(frame, lines):
    """
    Detect gray and black borders around detected lines.
    """
    for (x1, y1), (x2, y2) in lines:
        # Extract a small patch around the line to check for border colors
        margin = 5
        x1m, y1m = max(0, x1 - margin), max(0, y1 - margin)
        x2m, y2m = min(frame.shape[1] - 1, x2 + margin), min(frame.shape[0] - 1, y2 + margin)

        patch = frame[y1m:y2m, x1m:x2m]

        if patch.size == 0:
            continue

        # Convert patch to grayscale
        patch_gray = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY)

        # Define gray/black color range
        black_lower, black_upper = 0, 50
        gray_lower, gray_upper = 51, 150

        # Count pixels in range
        black_pixels = np.sum((patch_gray >= black_lower) & (patch_gray <= black_upper))
        gray_pixels = np.sum((patch_gray >= gray_lower) & (patch_gray <= gray_upper))

        # If a significant portion of the patch is black/gray, mark it
        total_pixels = patch_gray.size
        if (black_pixels / total_pixels) > 0.3 or (gray_pixels / total_pixels) > 0.3:
            cv2.rectangle(frame, (x1m, y1m), (x2m, y2m), (255, 0, 0), 2)  # Blue rectangle for border detection

# Execute the processing
process_video_and_detect_lines(video_path, frames_folder, skip_frames=1)
