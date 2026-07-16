"""
Task 2: Menu Photo Resizer and Colour Channel Analyser
---------------------------------------------------------
Loads a food/menu image, resizes it to a standard 256x256 model-input
size, splits it into B, G, R channels, reports average intensity per
channel, displays each channel as a grayscale window, and prints a
summary of the dominant colour channel.

Usage:
    python task2_menu_photo_analyser.py <path_to_image>

If no path is given, it defaults to "food_image.jpg" in the current
working directory.
"""

import sys
import os
import cv2


TARGET_SIZE = (256, 256)  # (width, height) expected by cv2.resize


def load_image(image_path: str):
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Could not read image at '{image_path}'.")
        print("Please check that the file exists and the path is correct.")
        sys.exit(1)

    print(f"Successfully loaded image: '{image_path}'  (original shape: {image.shape})")
    return image


def resize_image(image):
    # cv2.INTER_AREA is preferred for shrinking images, as it uses pixel
    # area relation and avoids the aliasing artefacts nearest-neighbour
    # or linear interpolation can introduce when downsampling.
    resized = cv2.resize(image, TARGET_SIZE, interpolation=cv2.INTER_AREA)
    print(f"Resized image to {TARGET_SIZE[0]}x{TARGET_SIZE[1]} using cv2.INTER_AREA.")
    print(f"New shape: {resized.shape}\n")
    return resized


def analyse_channels(resized_image):
    # cv2 loads images in BGR order by default (not RGB)
    b_channel, g_channel, r_channel = cv2.split(resized_image)

    b_mean = round(float(b_channel.mean()), 2)
    g_mean = round(float(g_channel.mean()), 2)
    r_mean = round(float(r_channel.mean()), 2)

    print("--- Average Channel Intensities (0-255 scale) ---")
    print(f"Blue  channel average intensity  : {b_mean}")
    print(f"Green channel average intensity  : {g_mean}")
    print(f"Red   channel average intensity  : {r_mean}")
    print("---------------------------------------------------\n")

    return b_channel, g_channel, r_channel, b_mean, g_mean, r_mean


def display_images(resized_image, b_channel, g_channel, r_channel):
    cv2.namedWindow("Resized Image (256x256)", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Blue Channel", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Green Channel", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Red Channel", cv2.WINDOW_NORMAL)

    cv2.imshow("Resized Image (256x256)", resized_image)
    # Each single-channel array displays natively as grayscale
    cv2.imshow("Blue Channel", b_channel)
    cv2.imshow("Green Channel", g_channel)
    cv2.imshow("Red Channel", r_channel)

    print("Displaying resized image and channel breakdowns. Press any key to close...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def summarise_dominant_channel(b_mean, g_mean, r_mean):
    channel_means = {"Blue": b_mean, "Green": g_mean, "Red": r_mean}
    dominant_channel = max(channel_means, key=channel_means.get)
    dominant_value = channel_means[dominant_channel]

    interpretation = {
        "Red": "suggesting the dish likely has warm, reddish tones (e.g. tomato-based sauces, "
               "meat, chili, or spice-heavy dishes).",
        "Green": "suggesting the dish likely has notable fresh or vegetal content "
                 "(e.g. leafy greens, herbs, or vegetable-forward plating).",
        "Blue": "which is uncommon for food (few dishes are naturally blue-dominant); this may "
                "indicate lighting conditions, plateware/background colour, or shadows influencing "
                "the image rather than the food itself.",
    }

    print(f"Summary: The {dominant_channel} channel has the highest average intensity "
          f"({dominant_value}), {interpretation[dominant_channel]}")


if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "food_image.jpg"

    if not os.path.exists(input_path):
        print(f"Error: File not found at '{input_path}'.")
        print("Tip: pass the image path as an argument, e.g.:")
        print("     python task2_menu_photo_analyser.py path/to/your_food_image.jpg")
        sys.exit(1)

    img = load_image(input_path)
    resized_img = resize_image(img)
    b, g, r, b_avg, g_avg, r_avg = analyse_channels(resized_img)
    display_images(resized_img, b, g, r)
    summarise_dominant_channel(b_avg, g_avg, r_avg)
