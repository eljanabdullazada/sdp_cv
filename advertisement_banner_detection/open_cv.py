import openai
import cv2
import numpy as np

# Set your OpenAI API key
openai.api_key = "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"

# Function to check for potential advertisement banners in the image
def detect_banner(image_path):
    """
    This function performs a simple heuristic-based detection for advertisement banners.
    It checks for large rectangular regions with distinct colors (as banners often have solid backgrounds).
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        return "Error: Unable to load the image."

    # Convert the image to grayscale for processing
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Analyze contours to detect rectangular shapes
    banner_detected = False
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:  # Check if the shape is a rectangle
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            # Heuristic: Banner-like regions are wide rectangles
            if w > 200 and h > 50 and aspect_ratio > 3:
                banner_detected = True
                break

    return "Detected" if banner_detected else "Not Detected"

# Path to the image
image_path = "frame_145.png"  # Replace with your image filename

# Step 1: Detect banner locally
banner_result = detect_banner(image_path)
print(f"Local Banner Detection Result: {banner_result}")

# Step 2: Send result to GPT for further analysis
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an assistant analyzing image-related features."},
        {"role": "user", "content": f"The local analysis of the image resulted in the following banner detection status: {banner_result}. Based on this, can you provide further insights or recommendations?"}
    ]
)

# Print GPT's response
print("GPT Response:")
print(response["choices"][0]["message"]["content"])
