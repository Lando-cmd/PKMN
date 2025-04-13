import os
import random
from barcode import UPCA
from barcode.writer import ImageWriter


def generate_barcode():
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
    return barcode_number  # Return just the barcode number


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