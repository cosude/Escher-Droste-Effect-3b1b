import cv2
import numpy as np

class DrosteImage:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise FileNotFoundError(f"Could not load image at {image_path}")
            
        self.height, self.width = self.image.shape[:2]
        
        self.center = None
        self.inner_w = None
        self.S = None

    def interactive_setup(self):
        """Runs the bounding box selection and calculates center and width."""
        print("--- DROSTE INTERACTIVE SETUP ---")
        print("1. Drag a box around the inner frame.")
        print("2. Press SPACE or ENTER to confirm your selection.")
        print("3. Press 'c' to cancel.")
        
        window_name = "Select Inner Frame"
        roi = cv2.selectROI(window_name, self.image, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow(window_name)
        
        x, y, w, h = roi
        
        if w == 0 or h == 0:
            return False
            
        self.inner_w = w
        self.center = (x + w // 2, y + h // 2)
        
        print(f"Bounding Box Selected: Width={w}px, Height={h}px")
        print(f"Calculated Center (Vanishing Point): {self.center}")
        
        self._calculate_params()
        return True

    def _calculate_params(self):
        """Computes the core zoom factor for the transformation."""
        self.S = self.width / self.inner_w
        print(f"Calculated S (Zoom Factor): {self.S:.4f}")

    def get_data(self):
        """Returns all preprocessed data for the simulation."""
        return {
            "img": self.image,
            "h": self.height,
            "w": self.width,
            "center": self.center,
            "inner_w": self.inner_w,
            "S": self.S
        }