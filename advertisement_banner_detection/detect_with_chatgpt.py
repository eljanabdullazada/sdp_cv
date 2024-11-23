import os

# Create a directory in a platform-independent way
dir_name = os.path.join(os.getcwd(), "example_dir")
os.makedirs(dir_name, exist_ok=True)

print(f"Directory created: {dir_name}")

from PIL import Image
import openai  # Corrected import statement
import base64

# Set your OpenAI API key here
openai.api_key = "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"

# Path to the image to be processed
IMAGE_PATH = r"C:\Users\user\Desktop\sdp_cv\advertisement_banner_detection\data\frames\frame_2.jpg"  # Replace with the actual image path

# Open the image file and encode it as a base64 string
def encode_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Error: The file at {image_path} was not found.")
        return None

# Process an image using ChatGPT
def process_image_with_chatgpt(base64_image):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Could you please detect if there have any banners."},
                {"role": "user", "content": f"Here is the image data: {base64_image}. Can you detect?"}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error during API call: {e}")
        return None

# Main function to encode and process the image
if __name__ == "__main__":
    # Encode the image
    base64_image = encode_image(IMAGE_PATH)
    if base64_image:
        # Process the image
        result = process_image_with_chatgpt(base64_image)
        if result:
            print("AI Response:", result)
        else:
            print("Failed to process the image with ChatGPT.")
    else:
        print("Image encoding failed.")