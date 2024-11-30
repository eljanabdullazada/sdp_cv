import openai
import base64

# Your OpenAI API key
api_key = "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"

# Set OpenAI API key
openai.api_key = api_key

# File path
file_path = "frame_145.png"

# Convert image to Base64
with open(file_path, "rb") as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

# Prepare the payload
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are an assistant analyzing images."},
        {
            "role": "user",
            "content": f"Check if there is an advertisement banner in the attached image. Here is the image data in base64 format: {image_base64}"
        }
    ]
)

# Print the response
print(response)
