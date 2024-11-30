import os
import pyimgur

# Imgur Client ID
IMGUR_CLIENT_ID = "a28dd9521bd04aa"

def upload_image_to_imgur(image_path):
    """Upload an image to Imgur and return its URL."""
    try:
        # Initialize Imgur client with your client ID
        im = pyimgur.Imgur(IMGUR_CLIENT_ID)

        # Upload image
        uploaded_image = im.upload_image(image_path, title="Uploaded with PyImgur")

        # Return the image URL
        return uploaded_image.link
    except Exception as e:
        print(f"Error uploading image to Imgur: {e}")
        return None

def upload_images_in_directory(directory):
    """Upload all image files in a given directory to Imgur."""
    # List all files in the directory
    for file_name in sorted(os.listdir(directory)):
        # Check if file is an image (you can modify this to include more formats if needed)
        if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(directory, file_name)
            print(f"Uploading {file_name} to Imgur...")

            # Upload the image
            image_url = upload_image_to_imgur(image_path)

            if image_url:
                print(f"Image uploaded successfully! URL: {image_url}")
            else:
                print(f"Failed to upload {file_name}.")
        else:
            print(f"Skipping non-image file: {file_name}")

if __name__ == "__main__":
    # Specify the directory containing images (corrected path)
    images_directory = "./data/frames"  # Correct relative path to the data folder
    upload_images_in_directory(images_directory)
