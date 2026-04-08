from ultralytics import YOLO

class HumanDetector:
    def __init__(self, model_path="yolov8n.pt"):
        """
        model_path: YOLO model file
        yolov8n = nano (fastest, lightweight)
        """
        self.model = YOLO(model_path)

    def detect(self, frame):
        """
        Returns:
        - frame (with bounding boxes)
        - human_detected (True/False)
        """

        results = self.model(frame, verbose=False)

        human_detected = False

        for result in results:
            boxes = result.boxes

            for box in boxes:
                cls = int(box.cls[0])

                # Class 0 = person in COCO dataset
                if cls == 0:
                    human_detected = True

                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # Draw bounding box
                    import cv2
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                    cv2.putText(
                        frame,
                        "Human",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 0, 0),
                        2
                    )

        return frame, human_detected