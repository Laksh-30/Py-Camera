import cv2

class MotionDetector:
    def __init__(self, min_area=1500, alpha=0.02):
        """
        min_area: minimum contour size to detect motion
        alpha: learning rate for background update
               smaller = slower adaptation (more stable)
               larger = faster adaptation (more responsive)
        """
        self.background = None
        self.min_area = min_area
        self.alpha = alpha

    def detect(self, frame):
        motion_detected = False

        # Step 1: Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Step 2: Blur to reduce noise
        gray = cv2.GaussianBlur(gray, (9, 9), 0)

        # Step 3: Initialize background
        if self.background is None:
            # Convert to float for running average
            self.background = gray.astype("float")
            return frame, motion_detected

        # Step 4: Update background (running average)
        cv2.accumulateWeighted(gray, self.background, self.alpha)

        # Step 5: Compute difference between current frame and background
        frame_delta = cv2.absdiff(gray, cv2.convertScaleAbs(self.background))

        # Step 6: Threshold
        thresh = cv2.threshold(frame_delta, 15, 255, cv2.THRESH_BINARY)[1]

        # Step 7: Morphological operations to remove noise
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Step 8: Find contours
        contours, _ = cv2.findContours(
            thresh.copy(),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        for contour in contours:
            if cv2.contourArea(contour) < self.min_area:
                continue

            motion_detected = True

            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        return frame, motion_detected