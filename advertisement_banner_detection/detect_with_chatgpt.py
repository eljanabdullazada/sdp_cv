<<<<<<< HEAD
import base64
import requests


# Function to read the Base64 string from the text file
def read_base64_from_file(file_path):
    with open(file_path, "r") as file:
        base64_string = file.read().strip()  # Read and remove any extra whitespace
    return base64_string


# Function to analyze the image using GPT-4 with the Base64 image data (GPT-4 Vision)
def analyze_image_with_gpt4_vision(base64_image_data):
    """Send the Base64 image data to GPT-4 Vision for analysis."""

    # Prepare the payload for the request
    payload = {
        "model": "gpt-4o",  # Specify the vision model (if using GPT-4 with vision capabilities)
        "messages": [
            {
                "role": "user",
                "content": "What’s in this image?"
            },
            {
                "role": "user",
                "content": base64_image_data  # Directly use the Base64 image data as the content
            }
        ],
        "max_tokens": 300
    }

    # Headers for the request with your API key directly
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer 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"  # Replace with your OpenAI API key
    }

    # Send the request to OpenAI API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()  # Process the response
    else:
        print(f"Error analyzing image: {response.text}")
        return None


# Main function to combine everything
def main():
    base64_file_path = "image_145_base64.txt"  # Path to the file containing Base64 image data

    # Read the Base64 string from the file
    base64_image_data = read_base64_from_file(base64_file_path)

    # Analyze the image using GPT-4 Vision (passing the Base64 image data here for analysis)
    analysis_result = analyze_image_with_gpt4_vision(base64_image_data)

    if analysis_result:
        print("Image analyzed successfully:", analysis_result)
    else:
        print("Failed to analyze image.")


# Run the script
if __name__ == "__main__":
    main()
=======

from PIL import Image
import openai  # Corrected import statement
import base64

import os
# Create a directory in a platform-independent way
dir_name = os.path.join(os.getcwd(), "example_dir")
os.makedirs(dir_name, exist_ok=True)
print(f"Directory created: {dir_name}")

# Set your OpenAI API key here
openai.api_key = os.getenv("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")

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
>>>>>>> toghrul
