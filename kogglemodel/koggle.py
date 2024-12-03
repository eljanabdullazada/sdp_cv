import torch
from sam2.sam2_video_predictor import SAM2VideoPredictor
import cv2
import numpy as np

# Load the pre-trained SAM 2 model
predictor = SAM2VideoPredictor.from_pretrained("facebook/sam2-hiera-base-plus")

# Video file to process
video_path = "C:/Users/user/Downloads/sdp_cv/advertisement_banner_detection/data/videos/dashcam_video.mp4"

# Initialize the model's state with the video
with torch.inference_mode():
    with torch.autocast("cuda", dtype=torch.bfloat16):
        state = predictor.init_state(video_path)
        
        # Define bounding box coordinates (example values)
        x_min, y_min, x_max, y_max = 50, 100, 200, 300
        
        # Add prompts to identify advertisement banners
        prompts = [
            {"type": "box", "coordinates": [x_min, y_min, x_max, y_max]},
        ]
        
        # Add prompts to the current frame
        frame_idx, object_ids, masks = predictor.add_new_points_or_box(state, prompts)
        
        # Propagate segmentation throughout the video
        for frame_idx, object_ids, masks in predictor.propagate_in_video(state):
            print(f"Frame {frame_idx}: Detected objects {object_ids}")
            
            # Save or process masks as needed
            mask_filename = f"output/mask_frame_{frame_idx}.png"
            
            # Convert mask to a format suitable for saving
            mask = masks[0].cpu().numpy().astype(np.uint8) * 255  # Assuming binary mask
            
            # Save mask using OpenCV
            cv2.imwrite(mask_filename, mask)
