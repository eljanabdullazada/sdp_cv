import cv2
import os


def extract_frames(video_path, frame_dir, nth_frame=30):
    # Create frame directory if it doesn't exist
    os.makedirs(frame_dir, exist_ok=True)

    # Open video
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    saved_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Save every nth frame
        if frame_count % nth_frame == 0:
            frame_path = os.path.join(frame_dir, f"frame_{saved_count}.jpg")
            cv2.imwrite(frame_path, frame)
            saved_count += 1

        frame_count += 1

    cap.release()
    print(f"Extracted {saved_count} frames from {video_path}")


# Example usage:
if __name__ == "__main__":
    extract_frames("advertisement_banner_detection/data/videos/IMG_0323.mp4", "data/frames", nth_frame=30)
