"""
Task 3: Packaging Label Transformer and Edge Scanner
---------------------------------------------------------
Loads a food packaging image, normalises its orientation and ROI through
a rotate -> crop -> flip chain, then applies Gaussian blur + Canny edge
detection to prepare the nutrition label region for OCR.

Usage:
    python task3_label_transformer.py <path_to_image>

If no path is given, it defaults to "food_image.jpg" in the current
working directory.
"""

import sys
import os
import cv2


def load_image(image_path: str):
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Could not read image at '{image_path}'.")
        print("Please check that the file exists and the path is correct.")
        sys.exit(1)

    print(f"Successfully loaded image: '{image_path}'  (shape: {image.shape})")
    return image


def rotate_90_clockwise(image):
    """
    Rotate the image 90 degrees clockwise using an explicit rotation
    matrix + warpAffine (rather than cv2.rotate) as required.
    A clockwise rotation corresponds to a NEGATIVE angle in OpenCV's
    convention (positive angles rotate counter-clockwise).
    """
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    angle = -90.0   # clockwise
    scale = 1.0
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)

    # Because a 90-degree rotation swaps width and height, we must
    # adjust the output canvas size and translation, otherwise the
    # rotated content gets clipped at the original width x height frame.
    new_w, new_h = h, w
    rotation_matrix[0, 2] += (new_w / 2) - center[0]
    rotation_matrix[1, 2] += (new_h / 2) - center[1]

    rotated = cv2.warpAffine(image, rotation_matrix, (new_w, new_h))

    print(f"Rotated image 90 degrees clockwise. New shape: {rotated.shape}")
    return rotated


def crop_lower_right_quadrant(image):
    h, w = image.shape[:2]
    mid_h, mid_w = h // 2, w // 2

    # NumPy slicing: rows (height) first, then columns (width)
    cropped = image[mid_h:h, mid_w:w]

    print(f"Cropped lower-right quadrant. New shape: {cropped.shape}")
    return cropped


def flip_horizontal(image):
    # flipCode = 1 -> horizontal flip
    flipped = cv2.flip(image, 1)
    print(f"Flipped cropped region horizontally. Shape: {flipped.shape}")
    return flipped


def display_step(window_title, image):
    cv2.namedWindow(window_title, cv2.WINDOW_NORMAL)
    cv2.imshow(window_title, image)


def apply_blur_and_edges(image):
    # Gaussian blur suppresses noise before gradient-based edge detection,
    # preventing sensor noise / label texture from producing false edges.
    blurred = cv2.GaussianBlur(image, (5, 5), sigmaX=0)

    # Convert to grayscale first if the image is still 3-channel, since
    # Canny expects a single-channel input.
    if len(blurred.shape) == 3:
        gray_for_edges = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    else:
        gray_for_edges = blurred

    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(gray_for_edges, low_threshold, high_threshold)

    print(f"Applied Gaussian blur (5x5, sigmaX=0) and Canny edge detection "
          f"(low={low_threshold}, high={high_threshold}).")
    return edges


if __name__ == "__main__":
    input_path = sys.argv[1] if len(sys.argv) > 1 else "food_image.jpg"

    if not os.path.exists(input_path):
        print(f"Error: File not found at '{input_path}'.")
        print("Tip: pass the image path as an argument, e.g.:")
        print("     python task3_label_transformer.py path/to/your_label_image.jpg")
        sys.exit(1)

    img = load_image(input_path)

    # --- Step 1: Rotate ---
    rotated_img = rotate_90_clockwise(img)
    display_step("Step 1 - Rotated 90deg Clockwise", rotated_img)

    # --- Step 2: Crop ---
    cropped_img = crop_lower_right_quadrant(rotated_img)
    display_step("Step 2 - Cropped Lower-Right Quadrant", cropped_img)

    # --- Step 3: Flip ---
    flipped_img = flip_horizontal(cropped_img)
    display_step("Step 3 - Flipped Horizontally", flipped_img)

    print("\nDisplaying rotate/crop/flip steps. Press any key to proceed to edge detection...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # --- Step 4: Blur + Canny edge detection ---
    edge_map = apply_blur_and_edges(flipped_img)

    cv2.namedWindow("Label Edges", cv2.WINDOW_NORMAL)
    cv2.imshow("Label Edges", edge_map)
    print("Displaying final edge map. Press any key to close and save...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # --- Step 5: Save edge map ---
    output_filename = "label_edges.jpg"
    success = cv2.imwrite(output_filename, edge_map)

    if success:
        print(f"Edge map saved successfully as '{output_filename}'")
    else:
        print(f"Error: Failed to save edge map as '{output_filename}'")
        sys.exit(1)
