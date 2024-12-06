import openai
client = openai.OpenAI()

# # Your OpenAI API key
# api_key = "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"
#
# # Set OpenAI API key
# openai.api_key = api_key

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages = [
        {
            "role" : "user",
            "content" :
            [
                {"type" : "text", "text" : "What's in this image?"},
                {
                    "type" : "image_url",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
                }
            ]
        }
    ],
    max_tokens = 300
)

print(response.choices[0].message.content)