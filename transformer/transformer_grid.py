import numpy as np

import numpy as np
import cv2

def _complex_to_flipped_maps(Z, center_x, center_y):
    map_x = Z.real + center_x
    map_y = Z.imag + center_y
    map_x = np.flip(map_x, axis=(0, 1))
    map_y = np.flip(map_y, axis=(0, 1))
    return map_x.astype(np.float32), map_y.astype(np.float32)


class DrosteEngine:
    def __init__(self, out_width, out_height, center_x, center_y, inner_width, zoom_factor, log_view_tiles=3.14):
        self.zoom_factor = zoom_factor
        self.R_min = inner_width / 2.0
        self.ln_r_period = np.log(zoom_factor)
        self.alpha = self.ln_r_period / (2 * np.pi)
        self.center_x = center_x
        self.center_y = center_y
        
        y, x = np.indices((out_height, out_width), dtype=np.float64)
        Z = (x - center_x) + 1j * (y - center_y)
        Z[Z == 0] = 1e-8 + 1e-8j
        
        self.ln_Z = np.log(Z)
        
        ln_r_start = np.log(self.R_min) - (log_view_tiles - 1.0) * (self.ln_r_period / 2.0)
        theta_start = -np.pi * log_view_tiles
        
        grid_ln_r = (x / out_width) * (self.ln_r_period * log_view_tiles) + ln_r_start
        grid_theta = (y / out_height) * (2 * np.pi * log_view_tiles) + theta_start 
        
        self.W_log = grid_ln_r + 1j * grid_theta
        
        self.map1 = ((np.exp(self.W_log).real + center_x).astype(np.float32), 
                     (np.exp(self.W_log).imag + center_y).astype(np.float32))

    def get_static_maps(self, c=1.0):
        P = c + 1j * self.alpha
        Z_src = np.exp(P * self.ln_Z)
        
        M = np.maximum(np.abs(Z_src.real), np.abs(Z_src.imag))
        M = np.where(M == 0, 1e-8, M)
        
        k = np.floor(np.log(M / self.R_min) / self.ln_r_period)
        scale = self.zoom_factor ** (-k)
        Z_wrapped = Z_src * scale
        
        return _complex_to_flipped_maps(Z_wrapped, self.center_x, self.center_y)

    def get_slanted_map(self, c=1.0):
        P = c + 1j * self.alpha
        Z_slanted = np.exp(self.W_log * P)
        
        map2 = ((Z_slanted.real + self.center_x).astype(np.float32), 
                (Z_slanted.imag + self.center_y).astype(np.float32))
        return self.map1, map2

    def get_zoom_frame(self, t, c=1.0, zoom_in=True):
        direction = 1 if zoom_in else -1
        
        P = c + 1j * self.alpha
        Z_src = np.exp(P * self.ln_Z)
        
        Z_scaled = Z_src * (self.zoom_factor ** (-t * direction))
        
        M_scaled = np.maximum(np.abs(Z_scaled.real), np.abs(Z_scaled.imag))
        M_scaled = np.where(M_scaled == 0, 1e-8, M_scaled)
        
        k_dynamic = np.floor(np.log(M_scaled / self.R_min) / self.ln_r_period)
        
        Z_final = Z_scaled * (self.zoom_factor ** -k_dynamic)
        return _complex_to_flipped_maps(Z_final, self.center_x, self.center_y)


def run_realtime_ui(image_path):
    img = cv2.imread(image_path)
    h, w = img.shape[:2]
    
    engine = DrosteEngine(
        out_width=w, out_height=h, 
        center_x=w/2, center_y=h/2, 
        inner_width=w/4, zoom_factor=2.0
    )
    
    window_name = "Droste Manipulator"
    cv2.namedWindow(window_name)
    cv2.createTrackbar("Constant m", window_name, 40, 60, lambda x: None)
    
    while True:
        slider = cv2.getTrackbarPos("Constant m", window_name)
        c = (slider - 30) / 10.0 
        
        map_x, map_y = engine.get_static_maps(c=c)
        result = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)
        
        cv2.imshow(window_name, result)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()