from utils.camera import get_camera
from motion.detector import MotionDetector
from detection.human_detector import HumanDetector
from capture.saver import ImageSaver

import cv2
import time


def main():
    """
    Main function that runs the smart surveillance system.
    Handles:
    - Camera feed
    - Motion detection
    - Human detection (YOLO)
    - Image capture
    - Alerts
    """

    # -------------------------------
    # 🎥 Initialize camera
    # -------------------------------
    cap = get_camera(0)

    # -------------------------------
    # 🧠 Initialize modules
    # -------------------------------
    motion_detector = MotionDetector(min_area=150, alpha=0.02)
    human_detector = HumanDetector()
    saver = ImageSaver()   # handles saving images

    # -------------------------------
    # ⏱️ Timing control (IMPORTANT)
    # -------------------------------

    # Prevents console spam for alerts
    last_alert_time = 0
    alert_cooldown = 2  # seconds

    # Prevents saving too many images
    last_capture_time = 0
    capture_cooldown = 5  # seconds

    # Optional: keep "human detected" state for a short time
    last_human_time = 0
    human_hold_time = 2  # seconds

    # Frame counter for optimization (YOLO skipping)
    frame_count = 0

    # -------------------------------
    # 🔁 Main loop
    # -------------------------------
    while True:
        ret, frame = cap.read()

        # If frame not received properly → exit
        if not ret:
            print("❌ Failed to grab frame")
            break

        # Resize for performance (IMPORTANT)
        frame = cv2.resize(frame, (640, 480))

        # -------------------------------
        # Step 1: Motion detection
        # -------------------------------
        frame, motion = motion_detector.detect(frame)

        # -------------------------------
        # Step 2: Human detection (YOLO)
        # -------------------------------
        frame_count += 1
        human = False

        # Run YOLO every 5 frames (performance optimization)
        if frame_count % 5 == 0:
            frame, human = human_detector.detect(frame)

            # If human detected → update last seen time
            if human:
                last_human_time = time.time()

        # Hold human state for a short duration (avoids flicker)
        if time.time() - last_human_time < human_hold_time:
            human = True

        # -------------------------------
        # Step 3: Timestamp
        # -------------------------------
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        cv2.putText(
            frame,
            timestamp,
            (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),  # yellow
            2
        )

        # -------------------------------
        # Step 4: Status display
        # -------------------------------
        if human:
            status = "🚨 HUMAN DETECTED"
            color = (0, 0, 255)  # red
        elif motion:
            status = "Motion (No Human)"
            color = (0, 255, 255)  # yellow
        else:
            status = "No Motion"
            color = (0, 255, 0)  # green

        cv2.putText(
            frame,
            status,
            (10, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

        # -------------------------------
        # Step 5: Alert logic (console)
        # -------------------------------
        current_time = time.time()

        if human and (current_time - last_alert_time > alert_cooldown):
            print(f"🚨 HUMAN DETECTED at {timestamp}")
            last_alert_time = current_time

        # -------------------------------
        # Step 6: Image capture logic
        # -------------------------------
        if human and (current_time - last_capture_time > capture_cooldown):
            filename = saver.save(frame)
            print(f"📸 Image saved: {filename}")
            last_capture_time = current_time

        # -------------------------------
        # Step 7: Show video feed
        # -------------------------------
        cv2.imshow("Smart Surveillance", frame)

        # Press 'q' to quit
        if cv2.waitKey(1) == ord("q"):
            break

    # -------------------------------
    # 🧹 Cleanup
    # -------------------------------
    cap.release()
    cv2.destroyAllWindows()


# Entry point
if __name__ == "__main__":
    main()