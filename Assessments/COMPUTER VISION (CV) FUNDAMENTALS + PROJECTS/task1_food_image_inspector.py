"""
Task 1: Food Image Loader and Inspector
-----------------------------------------
Loads a food image from disk, prints its basic properties (height, width,
channels), converts it to grayscale, displays both versions, and saves
the grayscale copy to disk.

Usage:
    python task1_food_image_inspector.py <path_to_image>

If no path is given, it defaults to "food_image.jpg" in the current
working directory.
"""

import sys
import os
import cv2


def load_and_inspect_image(image_path: str) -> None:
    # ---- 1. Load the image ----
    image = cv2.imread(image_path)

    # ---- 2. Verify it was read successfully ----
    if image is None:
        print(f"Error: Could not read image at '{image_path}'.")
        print("Please check that the file exists and the path is correct.")
        sys.exit(1)

    print(f"Successfully loaded image: '{image_path}'")

    # ---- 3. Print basic properties from .shape ----
    # Note: .shape returns (height, width, channels) for a color image,
    # or (height, width) for a single-channel grayscale image.
    shape = image.shape
    height = shape[0]
    width = shape[1]
    channels = shape[2] if len(shape) == 3 else 1

    print("\n--- Image Properties ---")
    print(f"Height        : {height} px")
    print(f"Width         : {width} px")
    print(f"Channels      : {channels}")
    print(f"Full shape    : {shape}")
    print(f"Data type     : {image.dtype}")
    print("------------------------\n")

    # ---- 4. Convert to grayscale ----
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # ---- 5. Display both versions in separate named windows ----
    cv2.namedWindow("Original - Color", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Converted - Grayscale", cv2.WINDOW_NORMAL)

    cv2.imshow("Original - Color", image)
    cv2.imshow("Converted - Grayscale", gray_image)

    print("Displaying images. Press any key (while a window is focused) to close them...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # ---- 6. Save the grayscale image to disk ----
    output_filename = "grayscale_food.jpg"
    success = cv2.imwrite(output_filename, gray_image)

    if success:
        print(f"Grayscale image saved successfully as '{output_filename}'")
    else:
        print(f"Error: Failed to save grayscale image as '{output_filename}'")
        sys.exit(1)


if __name__ == "__main__":
    # Accept an image path from the command line, or fall back to a default
    input_path = sys.argv[1] if len(sys.argv) > 1 else "food_image.jpg"

    if not os.path.exists(input_path):
        print(f"Error: File not found at '{input_path}'.")
        print("Tip: pass the image path as an argument, e.g.:")
        print("     python task1_food_image_inspector.py path/to/your_food_image.jpg")
        sys.exit(1)

    load_and_inspect_image(input_path)
