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
