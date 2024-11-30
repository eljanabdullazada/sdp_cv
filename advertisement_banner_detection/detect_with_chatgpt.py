import os
import openai

# OpenAI API Key
openai.api_key = "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"


def analyze_image_url(image_url):
    """Send image URL to GPT-4 for analysis."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that analyzes image URLs for specific details."},
                {"role": "user", "content": f"Analyze the following image: {image_url}"}
            ],
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error analyzing image URL: {e}")
        return None


def process_image_urls_from_file(file_path):
    """Process image URLs from the specified text file."""
    try:
        with open(file_path, 'r') as file:
            image_urls = file.readlines()

        # Iterate over the URLs and analyze them
        for image_url in image_urls:
            image_url = image_url.strip()  # Remove any extra whitespace or newline characters
            if image_url:
                print(f"Analyzing image URL: {image_url}")
                result = analyze_image_url(image_url)

                if result:
                    print(f"Analysis result: {result}")
                else:
                    print(f"Failed to analyze the image at {image_url}. Skipping...")
            else:
                print("Empty URL found in the file. Skipping...")
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Path to the image URLs text file
    image_urls_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "frames", "image_urls.txt")

    # Process the URLs from the file
    process_image_urls_from_file(image_urls_file)
