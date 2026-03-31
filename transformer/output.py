import cv2
import os
import numpy as np

def run_transformation(original_img, map_x, map_y):
    result = cv2.remap(original_img, map_x, map_y, cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
    display_img = result.copy()

    cv2.putText(display_img, "Press ANY KEY to return to menu", (30, 50), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.imshow("Droste Math Visualizer", display_img)
    cv2.waitKey(0)

    return result

def show_droste_stages(img, m1, m2, m3, gap_size=10, gap_color=(0, 0, 0)):
    img_log = cv2.remap(img, m1[0], m1[1], cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_WRAP)

    img_rot = cv2.remap(img, m2[0], m2[1], cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_WRAP)

    img_final = cv2.remap(img, m3[0], m3[1], cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
    
    tl = cv2.copyMakeBorder(img_log, gap_size, gap_size, gap_size, gap_size, cv2.BORDER_CONSTANT, value=gap_color)
    tr = cv2.copyMakeBorder(img, gap_size, gap_size, gap_size, gap_size, cv2.BORDER_CONSTANT, value=gap_color)
    bl = cv2.copyMakeBorder(img_rot, gap_size, gap_size, gap_size, gap_size, cv2.BORDER_CONSTANT, value=gap_color)
    br = cv2.copyMakeBorder(img_final, gap_size, gap_size, gap_size, gap_size, cv2.BORDER_CONSTANT, value=gap_color)

    grid = np.vstack((
        np.hstack((tl, tr)),
        np.hstack((bl, br))
    ))

    grid_h, grid_w = grid.shape[:2]
    target_w = 1000
    target_h = int(target_w * (grid_h / grid_w))

    display_grid = cv2.resize(grid, (target_w, target_h))

    cv2.putText(display_grid, "Press ANY KEY to return to menu", (30, 50), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow("Droste Math Visualizer", display_grid)
    cv2.waitKey(0)