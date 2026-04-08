from utils.camera import get_camera
from motion.detector import MotionDetector
from detection.human_detector import HumanDetector
from capture.saver import ImageSaver
from alerts.telegram import TelegramAlert

import cv2
import time
import threading


def main():
    """
    Smart Surveillance System
    - Motion detection
    - Human detection (YOLO)
    - Image capture
    - Telegram alerts (non-blocking)
    """

    # -------------------------------
    # 🎥 Camera
    # -------------------------------
    cap = get_camera(0)

    # -------------------------------
    # 🧠 Modules
    # -------------------------------
    motion_detector = MotionDetector(min_area=150, alpha=0.02)
    human_detector = HumanDetector()
    saver = ImageSaver()

    telegram = TelegramAlert(
        bot_token="8677721345:AAF3Rdx8ticqtkSG-BoyaZ7hXAXkYE1Ld3Q",
        chat_id="8277408775"
    )

    # -------------------------------
    # ⏱️ Control variables
    # -------------------------------
    last_alert_time = 0
    alert_cooldown = 2

    last_capture_time = 0
    capture_cooldown = 10  # increased to reduce spam

    last_human_time = 0
    human_hold_time = 2

    frame_count = 0

    # -------------------------------
    # 🧵 Telegram thread function
    # -------------------------------
    def send_telegram_alert(filename, timestamp):
        telegram.send_message(f"🚨 Human detected at {timestamp}")
        telegram.send_image(filename)

    # -------------------------------
    # 🔁 Main loop
    # -------------------------------
    while True:
        ret, frame = cap.read()

        if not ret:
            print("❌ Camera error")
            break

        # Resize → improves performance
        frame = cv2.resize(frame, (480, 360))

        # -------------------------------
        # Motion detection
        # -------------------------------
        frame, motion = motion_detector.detect(frame)

        # -------------------------------
        # Human detection (YOLO)
        # -------------------------------
        frame_count += 1
        human = False

        if frame_count % 10 == 0:  # reduced frequency → less lag
            frame, human = human_detector.detect(frame)

            if human:
                last_human_time = time.time()

        # Hold detection to avoid flicker
        if time.time() - last_human_time < human_hold_time:
            human = True

        # -------------------------------
        # Timestamp
        # -------------------------------
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        cv2.putText(frame, timestamp, (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

        # -------------------------------
        # Status
        # -------------------------------
        if human:
            status = "🚨 HUMAN DETECTED"
            color = (0, 0, 255)
        elif motion:
            status = "Motion (No Human)"
            color = (0, 255, 255)
        else:
            status = "No Motion"
            color = (0, 255, 0)

        cv2.putText(frame, status, (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # -------------------------------
        # Alerts (console)
        # -------------------------------
        current_time = time.time()

        if human and (current_time - last_alert_time > alert_cooldown):
            print(f"🚨 HUMAN DETECTED at {timestamp}")
            last_alert_time = current_time

        # -------------------------------
        # Capture + Telegram (threaded)
        # -------------------------------
        if human and (current_time - last_capture_time > capture_cooldown):

            filename = saver.save(frame)
            print(f"📸 Image saved: {filename}")

            # Run Telegram in background thread (NO LAG)
            threading.Thread(
                target=send_telegram_alert,
                args=(filename, timestamp),
                daemon=True
            ).start()

            last_capture_time = current_time

        # -------------------------------
        # Display
        # -------------------------------
        cv2.imshow("Smart Surveillance", frame)

        if cv2.waitKey(1) == ord("q"):
            break

    # -------------------------------
    # Cleanup
    # -------------------------------
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()