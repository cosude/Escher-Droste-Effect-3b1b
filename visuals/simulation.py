import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocessor import *

from transformer import *
from visuals.window import run_interactive_viewer


def run_simulation(image_path):
    data_provider = DrosteImage(image_path)
    
    if not data_provider.interactive_setup(): 
        print("Setup cancelled by user.")
        return

    data = data_provider.get_data()
    h, w = data['h'], data['w']
    cx, cy = data['center']
    original_img = data['img']
    inner_width = data['inner_w'] 
    zoom_factor = data['S']

    print("Generating Droste map... calculating coordinates.")

    m1, m2, zoom_provider = prepare_droste_data(
        w, h, cx, cy, inner_width, zoom_factor
    )
    
    m3 = zoom_provider(0)

    run_interactive_viewer(original_img, m1, m2, m3, zoom_provider)