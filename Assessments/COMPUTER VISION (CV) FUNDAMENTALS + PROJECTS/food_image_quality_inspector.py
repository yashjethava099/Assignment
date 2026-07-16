"""
Mini Project: Food Delivery Image Quality Inspector
---------------------------------------------------------
A menu-driven console utility that loads a food/menu/label image and
runs a standardised inspection pipeline:

    1. Load & inspect image
    2. Resize and analyse colour channels
    3. Apply transformation pipeline (rotate -> crop -> flip)
    4. Run edge-based quality scan
    5. Exit

Usage:
    python food_image_quality_inspector.py

The program will prompt for an image path when you choose Option 1.
All subsequent options operate on that same loaded image, so run
Option 1 first.
"""

import os
import sys
import cv2


class FoodImageInspector:
    def __init__(self):
        self.image = None          # original loaded BGR image
        self.image_path = None

    # ------------------------------------------------------------------
    # Option 1: Load & inspect image
    # ------------------------------------------------------------------
    def load_and_inspect(self):
        path = input("Enter the path to the food image: ").strip()

        if not os.path.exists(path):
            print(f"Error: File not found at '{path}'. Returning to menu.\n")
            return

        image = cv2.imread(path)

        if image is None:
            print(f"Error: Could not read image at '{path}'. "
                  f"It may be corrupted or an unsupported format. Returning to menu.\n")
            return

        self.image = image
        self.image_path = path

        shape = image.shape
        height = shape[0]
        width = shape[1]
        channels = shape[2] if len(shape) == 3 else 1

        print(f"\nSuccessfully loaded image: '{path}'")
        print("--- Image Properties ---")
        print(f"Height   : {height} px")
        print(f"Width    : {width} px")
        print(f"Channels : {channels}")
        print("-------------------------")

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        cv2.namedWindow("Original - Color", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Grayscale Version", cv2.WINDOW_NORMAL)
        cv2.imshow("Original - Color", image)
        cv2.imshow("Grayscale Version", gray_image)
        print("Displaying original and grayscale versions. Press any key to continue...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        base_name = os.path.splitext(os.path.basename(path))[0]
        output_filename = f"{base_name}_gray.jpg"
        success = cv2.imwrite(output_filename, gray_image)

        if success:
            print(f"Grayscale image saved as '{output_filename}'\n")
        else:
            print(f"Error: Failed to save grayscale image as '{output_filename}'\n")

    # ------------------------------------------------------------------
    # Option 2: Resize and analyse colour channels
    # ------------------------------------------------------------------
    def resize_and_analyse_channels(self):
        if not self._require_loaded_image():
            return

        resized = cv2.resize(self.image, (256, 256), interpolation=cv2.INTER_AREA)
        print(f"\nResized image to 256x256 using cv2.INTER_AREA.")

        b_channel, g_channel, r_channel = cv2.split(resized)

        b_mean = round(float(b_channel.mean()), 2)
        g_mean = round(float(g_channel.mean()), 2)
        r_mean = round(float(r_channel.mean()), 2)

        print("--- Average Channel Intensities (0-255 scale) ---")
        print(f"Blue  channel average intensity : {b_mean}")
        print(f"Green channel average intensity : {g_mean}")
        print(f"Red   channel average intensity : {r_mean}")
        print("---------------------------------------------------")

        channel_means = {"Blue": b_mean, "Green": g_mean, "Red": r_mean}
        dominant_channel = max(channel_means, key=channel_means.get)
        print(f"Dominant channel: {dominant_channel} "
              f"(average intensity {channel_means[dominant_channel]})\n")

        cv2.namedWindow("Resized Image (256x256)", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Blue Channel", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Green Channel", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Red Channel", cv2.WINDOW_NORMAL)

        cv2.imshow("Resized Image (256x256)", resized)
        cv2.imshow("Blue Channel", b_channel)
        cv2.imshow("Green Channel", g_channel)
        cv2.imshow("Red Channel", r_channel)

        print("Displaying resized image and channel breakdowns. Press any key to continue...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # ------------------------------------------------------------------
    # Option 3: Apply transformation pipeline (rotate -> crop -> flip)
    # ------------------------------------------------------------------
    def transformation_pipeline(self):
        if not self._require_loaded_image():
            return

        angle_input = input("Enter rotation angle in degrees (e.g. 45, -90): ").strip()
        try:
            angle = float(angle_input)
        except ValueError:
            print(f"Error: '{angle_input}' is not a valid number. Returning to menu.\n")
            return

        rotated = self._rotate_image(self.image, angle)
        cv2.namedWindow("Step 1 - Rotated", cv2.WINDOW_NORMAL)
        cv2.imshow("Step 1 - Rotated", rotated)
        print(f"\nRotated image by {angle} degrees. New shape: {rotated.shape}")

        cropped = self._crop_center_percent(rotated, percent=0.60)
        cv2.namedWindow("Step 2 - Center 60% Crop", cv2.WINDOW_NORMAL)
        cv2.imshow("Step 2 - Center 60% Crop", cropped)
        print(f"Cropped central 60% region. New shape: {cropped.shape}")

        flipped = cv2.flip(cropped, 1)
        cv2.namedWindow("Step 3 - Flipped Horizontally", cv2.WINDOW_NORMAL)
        cv2.imshow("Step 3 - Flipped Horizontally", flipped)
        print(f"Flipped horizontally. Final shape: {flipped.shape}")

        print("Displaying rotate/crop/flip steps. Press any key to continue...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print()

    @staticmethod
    def _rotate_image(image, angle):
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)

        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

        # Expand canvas so the rotated content isn't clipped at arbitrary
        # angles (standard "rotate without cropping" bounding-box fix).
        cos = abs(rotation_matrix[0, 0])
        sin = abs(rotation_matrix[0, 1])
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))

        rotation_matrix[0, 2] += (new_w / 2) - center[0]
        rotation_matrix[1, 2] += (new_h / 2) - center[1]

        rotated = cv2.warpAffine(image, rotation_matrix, (new_w, new_h))
        return rotated

    @staticmethod
    def _crop_center_percent(image, percent=0.60):
        h, w = image.shape[:2]
        crop_h = int(h * percent)
        crop_w = int(w * percent)

        start_y = (h - crop_h) // 2
        start_x = (w - crop_w) // 2

        cropped = image[start_y:start_y + crop_h, start_x:start_x + crop_w]
        return cropped

    # ------------------------------------------------------------------
    # Option 4: Run edge-based quality scan
    # ------------------------------------------------------------------
    def edge_based_quality_scan(self):
        if not self._require_loaded_image():
            return

        blurred = cv2.GaussianBlur(self.image, (5, 5), sigmaX=0)
        gray_blurred = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

        low_threshold = 50
        high_threshold = 150
        edges = cv2.Canny(gray_blurred, low_threshold, high_threshold)

        edge_pixel_count = cv2.countNonZero(edges)

        cv2.namedWindow("Edge Map", cv2.WINDOW_NORMAL)
        cv2.imshow("Edge Map", edges)
        print(f"\nApplied Gaussian blur (5x5) + Canny edge detection "
              f"(low={low_threshold}, high={high_threshold}).")
        print(f"Total edge pixels detected: {edge_pixel_count}")

        if edge_pixel_count > 5000:
            verdict = "High texture (good detail)"
        else:
            verdict = "Low texture (may need re-shoot)"

        print(f"Quality verdict: {verdict}")
        print("Displaying edge map. Press any key to continue...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _require_loaded_image(self):
        if self.image is None:
            print("No image loaded yet. Please run Option 1 first.\n")
            return False
        return True


def print_menu():
    print("=" * 55)
    print(" FOOD DELIVERY IMAGE QUALITY INSPECTOR")
    print("=" * 55)
    print("1. Load & inspect image")
    print("2. Resize and analyse colour channels")
    print("3. Apply transformation pipeline")
    print("4. Run edge-based quality scan")
    print("5. Exit")
    print("=" * 55)


def main():
    inspector = FoodImageInspector()

    while True:
        print_menu()
        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            inspector.load_and_inspect()
        elif choice == "2":
            inspector.resize_and_analyse_channels()
        elif choice == "3":
            inspector.transformation_pipeline()
        elif choice == "4":
            inspector.edge_based_quality_scan()
        elif choice == "5":
            print("Exiting Food Delivery Image Quality Inspector. Goodbye.")
            sys.exit(0)
        else:
            print(f"Invalid option '{choice}'. Please select a number between 1 and 5.\n")


if __name__ == "__main__":
    main()
