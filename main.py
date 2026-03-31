import tkinter as tk
from tkinter import filedialog
from visuals import *

def select_image():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select Image for Droste Effect",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.webp")]
    )
    
    if not file_path:
        print("No image selected. Exiting...")
        return None
    
    return file_path

if __name__ == "__main__":
    print("--- Droste Conformal Mapping Tool ---")
    image_path = select_image()
    
    if image_path:
        try:
            run_simulation(image_path)
        except Exception as e:
            print(f"An error occurred: {e}")
            input("Press Enter to close...")