import cv2

video_path = r"C:\Users\user\Desktop\sdp_cv-1\advertisement_banner_detection\data\videos\IMG_0323.mp4"

print(f"Attempting to open video: {video_path}")
cap = cv2.VideoCapture(video_path)

if cap.isOpened():
    print("Video opened successfully.")
    print(f"Frame width: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}")
    print(f"Frame height: {cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
    print(f"Frame rate: {cap.get(cv2.CAP_PROP_FPS)}")
    print(f"Frame count: {cap.get(cv2.CAP_PROP_FRAME_COUNT)}")
else:
    print("Error: Cannot open video.")
cap.release()
