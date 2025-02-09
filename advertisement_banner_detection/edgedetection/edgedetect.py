import cv2
import os
import numpy as np

# Paths
video_path = r"C:\Users\user\Desktop\sdp_cv-1\advertisement_banner_detection\data\videos\dashcam_video.mp4"
output_video_path = r"C:\Users\user\Desktop\sdp_cv-1\advertisement_banner_detection\data\output_video.avi"

# Ensure output folder exists
os.makedirs(os.path.dirname(output_video_path), exist_ok=True)

# Open input video
cap = cv2.VideoCapture(video_path)

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))  # Frames per second

# Define video writer with high quality
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Use 'XVID' or 'MJPG' for better quality
output_video = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

def process_frame(frame):
    """ Process frame: Detect long lines with right angles in the top-right corner """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Get dimensions
    height, width = edges.shape

    # Define the region of interest (top-right corner)
    roi_x_start = int(width * 0.5)  # Middle of width
    roi_x_end = width
    roi_y_start = 0
    roi_y_end = int(height * 0.5)  # Upper half of the frame

    cropped_edges = edges[roi_y_start:roi_y_end, roi_x_start:roi_x_end]
    frame_roi = frame[roi_y_start:roi_y_end, roi_x_start:roi_x_end]

    # Detect lines using Hough Transform
    lines = cv2.HoughLinesP(cropped_edges, rho=1, theta=np.pi/180, threshold=100, minLineLength=int(width * 0.15), maxLineGap=10)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]

            # Calculate length and height
            line_length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            line_height = abs(y2 - y1)

            # Ensure length is 15% of width & height is 10% of frame
            if line_length >= int(width * 0.15) and line_height <= int(height * 0.1) and line_length > line_height:
                cv2.line(frame_roi, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw green line

    # Replace processed region back into the frame
    frame[roi_y_start:roi_y_end, roi_x_start:roi_x_end] = frame_roi

    return frame

# Process video
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    processed_frame = process_frame(frame)
    output_video.write(processed_frame)  # Save frame to video

cap.release()
output_video.release()
cv2.destroyAllWindows()

print(f"Processing complete. Video saved at: {output_video_path}")
