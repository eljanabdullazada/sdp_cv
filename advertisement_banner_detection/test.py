import requests
import json

# Replace with your OpenAI API key
API_KEY = "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"

# URL of the image you want to analyze
image_url = "https://i.imgur.com/EQlBXQu.jpeg"

# Payload for the request
data = {
    "model": "gpt-4",  # Ensure you're using GPT-4
    "messages": [
        {
            "role": "user",
            "content": "What’s in this image?"
        },
        {
            "role": "user",
            "content": image_url  # Pass the URL directly as a string
        }
    ],
    "max_tokens": 300
}

# Headers for the request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Send the request to OpenAI API
response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(data))

# Check if the response is successful
if response.status_code == 200:
    analysis_result = response.json()
    print("Image Analysis Result:", analysis_result)
else:
    print(f"Error analyzing image: {response.text}")
