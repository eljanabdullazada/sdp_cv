# live_detect.py
import sys
from main import detect_banners

if __name__ == "__main__":
    video_path = sys.argv[1]
    detect_banners(video_path)
