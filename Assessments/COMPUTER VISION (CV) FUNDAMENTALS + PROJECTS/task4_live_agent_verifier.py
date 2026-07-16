"""
Task 4: Live Delivery Agent Face Verifier
---------------------------------------------------------
Opens the default webcam, runs real-time Haar cascade face detection on
each frame, draws a labelled bounding box around detected faces, and
lets the user save a snapshot ('s') or quit cleanly ('q').

Usage:
    python task4_live_agent_verifier.py

Controls:
    s -> save current frame as agent_snapshot.jpg
    q -> quit and release resources
"""

import sys
import cv2


WINDOW_TITLE = "Delivery Agent Verifier"
SNAPSHOT_FILENAME = "agent_snapshot.jpg"


def load_face_cascade():
    # Use the frontal face Haar cascade bundled with OpenCV's data directory
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)

    if face_cascade.empty():
        print(f"Error: Could not load Haar cascade from '{cascade_path}'.")
        print("Verify your OpenCV installation includes the haarcascades data files.")
        sys.exit(1)

    return face_cascade


def open_webcam():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open the default webcam (index 0).")
        print("Check that a camera is connected and not in use by another application.")
        sys.exit(1)

    return cap


def draw_detections(frame, faces):
    for (x, y, w, h) in faces:
        # Green bounding box around the detected face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Label text placed just above the bounding box
        label = "Agent Detected"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        thickness = 2
        text_y = y - 10 if y - 10 > 10 else y + 20  # keep label on-screen near top edge

        cv2.putText(frame, label, (x, text_y), font, font_scale,
                    (0, 255, 0), thickness, cv2.LINE_AA)

    return frame


def main():
    face_cascade = load_face_cascade()
    cap = open_webcam()

    print(f"Webcam opened. Displaying live feed in '{WINDOW_TITLE}'.")
    print("Press 's' to save a snapshot, or 'q' to quit.\n")

    cv2.namedWindow(WINDOW_TITLE, cv2.WINDOW_NORMAL)

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("Error: Failed to read frame from webcam. Exiting loop.")
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # minNeighbors=6 and minSize=(80,80) tuned to reduce false
            # positives from decor/background objects while still
            # catching a real face at typical doorbell distance.
            faces = face_cascade.detectMultiScale(
                gray_frame,
                scaleFactor=1.1,
                minNeighbors=6,
                minSize=(80, 80)
            )

            display_frame = draw_detections(frame.copy(), faces)
            cv2.imshow(WINDOW_TITLE, display_frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('s'):
                success = cv2.imwrite(SNAPSHOT_FILENAME, display_frame)
                if success:
                    print(f"Snapshot saved as '{SNAPSHOT_FILENAME}'")
                else:
                    print(f"Error: Failed to save snapshot as '{SNAPSHOT_FILENAME}'")

            elif key == ord('q'):
                print("Quit key pressed. Releasing resources...")
                break

    finally:
        # Ensure cleanup happens even if an error interrupts the loop
        cap.release()
        cv2.destroyAllWindows()
        print("Webcam released and all windows closed. Goodbye.")


if __name__ == "__main__":
    main()
