import os
import random
from barcode import UPCA
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont


def generate_barcode(card_name, card_condition):
    # Get the desktop directory of the current user
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    # Create a 'barcodes' directory on the desktop
    barcode_directory = os.path.join(desktop_path, "barcodes")
    os.makedirs(barcode_directory, exist_ok=True)

    # Generate a random 12-digit UPC-A barcode number
    barcode_number = "".join([str(random.randint(0, 9)) for _ in range(11)])
    check_digit = calculate_upc_check_digit(barcode_number)
    barcode_number += str(check_digit)

    # Generate the barcode and save it in the 'barcodes' folder
    barcode = UPCA(barcode_number, writer=ImageWriter())
    filename = os.path.join(barcode_directory, barcode_number)
    barcode.save(filename)

    # Open the generated barcode image
    barcode_image_path = f"{filename}.png"
    barcode_image = Image.open(barcode_image_path)

    # Add card name and condition to the barcode image
    updated_image_path = add_text_to_barcode(barcode_image, card_name, card_condition, barcode_image_path)

    # Return the barcode number and the updated image path
    return barcode_number, updated_image_path


def calculate_upc_check_digit(barcode_number):
    """
    Calculate the check digit for a UPC-A barcode.
    The check digit is calculated using the first 11 digits of the barcode.
    """
    odd_sum = sum(int(barcode_number[i]) for i in range(0, 11, 2))
    even_sum = sum(int(barcode_number[i]) for i in range(1, 11, 2))
    total = (odd_sum * 3) + even_sum
    check_digit = (10 - (total % 10)) % 10
    return check_digit


def add_text_to_barcode(barcode_image, card_name, card_condition, save_path):
    """
    Add the card name and condition as text below the barcode image.
    """
    # Create a new image with extra space for text
    new_width = barcode_image.width
    new_height = barcode_image.height + 50  # Add space for text
    new_image = Image.new("RGB", (new_width, new_height), "white")

    # Paste the barcode onto the new image
    new_image.paste(barcode_image, (0, 0))

    # Add text (card name and condition)
    draw = ImageDraw.Draw(new_image)

    try:
        # Use a default font (adjust font path if necessary)
        font = ImageFont.truetype("arial.ttf", 34)
    except IOError:
        # Fallback to default font if TTF font is not available
        font = ImageFont.load_default()

    text = f"{card_name} - {card_condition}"

    # Use textbbox to calculate text width and height
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    text_x = (new_width - text_width) // 2  # Center the text horizontally
    text_y = barcode_image.height + 5  # Place the text below the barcode
    draw.text((text_x, text_y), text, fill="black", font=font)

    # Save the new image with text
    new_image.save(save_path)
    return save_path
