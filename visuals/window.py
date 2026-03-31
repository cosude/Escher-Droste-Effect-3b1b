import cv2
import numpy as np
from visuals import *
from transformer import *

def run_interactive_viewer(img, m1, m2, m3, zoom_provider):
    window_name = "Droste Math Visualizer" 
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    def draw_main_menu():
        menu_frame = cv2.addWeighted(img, 0.3, np.zeros_like(img), 0.7, 0)
        
        cv2.putText(menu_frame, "Droste Math Visualizer", (50, 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3, cv2.LINE_AA)
        cv2.putText(menu_frame, "Select a Module:", (50, 140), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2, cv2.LINE_AA)
        
        cv2.putText(menu_frame, "[1] Final Static Result", (70, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36, 191, 124), 2)
        cv2.putText(menu_frame, "[2] Stages Grid", (70, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36, 191, 124), 2)
        cv2.putText(menu_frame, "[3] Pixel Animation", (70, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36, 191, 124), 2)
        cv2.putText(menu_frame, "[4] Full Animation Sequence", (70, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36, 191, 124), 2)
        cv2.putText(menu_frame, "[ESC] Quit Program", (70, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        return menu_frame

    try:
        while True:
            menu_frame = draw_main_menu()
            cv2.imshow(window_name, menu_frame)
            
            key = cv2.waitKey(0) & 0xFF

            if key == ord('1'):
                run_transformation(img, m3[0], m3[1]) 
                
            elif key == ord('2'):
                show_droste_stages(img, m1, m2, m3)

            elif key == ord('3'):
                animate_droste(img,m3[0],m3[1])

            elif key == ord('4'):
                animate_droste_steps(img, m1, m2, m3, zoom_provider)
                
            elif key == ord('q') or key == 27:
                break
                
    finally:
        cv2.destroyAllWindows()