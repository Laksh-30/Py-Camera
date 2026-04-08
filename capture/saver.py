import cv2
import os
from datetime import datetime

class ImageSaver:
    def __init__(self, save_dir="captures"):
        """
        save_dir: folder where images will be stored
        """
        self.save_dir = save_dir

        # Create folder if it doesn't exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

    def save(self, frame):
        """
        Saves the frame as an image with timestamp filename
        """

        # Generate timestamp-based filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"{self.save_dir}/capture_{timestamp}.jpg"

        # Save image
        cv2.imwrite(filename, frame)

        return filename