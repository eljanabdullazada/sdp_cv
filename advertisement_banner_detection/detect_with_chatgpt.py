import os
from PIL import Image
import openai

# Set your OpenAI API key here
openai.api_key = "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"

def process_frame_with_chatgpt(frame_content):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Specify the model you want to use
            messages=[
                {"role": "user", "content": frame_content}
            ]
        )
        return response['choices'][0]['message']['content']  # Adjust based on the response structure
    except Exception as e:
        print(f"Error during API call: {e}")
        return None

def detect_banners_in_frames(frames_directory, detections_directory, max_attempts=5):
    frame_files = sorted(os.listdir(frames_directory))
    attempts = 0  # Counter for attempts

    for frame_file in frame_files:
        if attempts >= max_attempts:
            break  # Stop processing if the maximum attempts have been reached

        frame_path = os.path.join(frames_directory, frame_file)
        print(f"Processing {frame_file} with ChatGPT model...")

        try:
            # Load and process the image (if needed)
            frame_content = f"Content of the image {frame_file}"  # Replace with actual content extraction logic

            result = process_frame_with_chatgpt(frame_content)
            if result:
                # Save result or do something with it
                print(f"Result for {frame_file}: {result}")
                attempts += 1  # Increment attempts after successful processing

        except Exception as e:
            print(f"Error processing {frame_file}: {e}")

if __name__ == "__main__":
    detect_banners_in_frames("data/frames", "data/detections", max_attempts=5)
