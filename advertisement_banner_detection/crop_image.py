from PIL import Image


def crop_top_right(image_path, output_path):
    """
    Crops the top-right quarter of the given image and saves it to the output path.

    :param image_path: Path to the input image.
    :param output_path: Path to save the cropped image.
    """
    # Open the image
    image = Image.open(image_path)
    width, height = image.size

    # Calculate the cropping coordinates
    left = width // 2  # Start at the middle of the width
    top = 0  # Start from the top
    right = width  # Go to the end of the width
    bottom = height // 2  # Go to the middle of the height

    # Crop the image
    cropped_image = image.crop((left, top, right, bottom))

    # Save the cropped image
    cropped_image.save(output_path)
    print(f"Cropped image saved to {output_path}")


# Example usage:
crop_top_right("frame_145.png", "cropped_image.jpg")
