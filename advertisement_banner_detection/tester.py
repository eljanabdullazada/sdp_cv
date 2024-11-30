import openai
import time
#for testing if api key and gpt works properly

# Replace with your actual API key
openai.api_key = "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"

def test_api_connection():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use a model available to the free tier
            messages=[{"role": "user", "content": "Hello!"}],
        )
        print("API response:", response.choices[0].message['content'])
    except openai.error.RateLimitError:
        print("Error: You have exceeded your current quota. Please check your plan and billing details.")
    except openai.error.OpenAIError as e:
        print(f"Error during API call: {e}")

if __name__ == "__main__":
    # Test the API connection
    for _ in range(5):  # Limit to 5 attempts
        test_api_connection()
        time.sleep(10)  # Wait for 10 seconds before the next request
