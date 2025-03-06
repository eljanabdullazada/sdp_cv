import requests
import base64

# API Key for OpenAI
API_KEY = "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"
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"  # Default ChatCompletion endpoint

<<<<<<< HEAD
# Path to your image
image_path = "frame_145.png"
=======
def test_api_connection():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use a model available to the free tier
            messages=[{"role": "user", "content": "Hello!"}],
        )
        print("API response:", response.choices[0].message['content'])
    except openai.error.RateLimitError:
        print("Error: You have exceeded your current quota. Please check your plan and billing details.")
    except openai.error.OpenAIError as e:
        print(f"Error during API call: {e}")
>>>>>>> toghrul

# Read and encode image in base64
with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

# Compose request headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Compose request payload
data = {
    "model": "gpt-4-vision-preview",  # Use the correct model name when Vision support is enabled
    "messages": [
        {"role": "user", "content": "What’s in this image?"}
    ],
    "files": [
        {
            "name": "image.jpg",
            "data": base64_image
        }
    ],
    "max_tokens": 300
}

# Make the request
response = requests.post(API_ENDPOINT, headers=headers, json=data)

# Check and print the response
if response.status_code == 200:
    print(response.json()["choices"][0]["message"]["content"])
else:
    print(f"Error {response.status_code}: {response.text}")
