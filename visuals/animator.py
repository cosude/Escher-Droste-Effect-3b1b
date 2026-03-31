import cv2
import numpy as np

def ease_in_out_quad(t):
    return 2 * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 2) / 2

def animate_droste(original_img, map_x, map_y):
    h, w = original_img.shape[:2]
    num_divs = 15
    fly_steps = 15
    step_delay = 1
    
    perfect_result = cv2.remap(original_img, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

    y_bounds = np.linspace(0, h, num_divs + 1).astype(int)
    x_bounds = np.linspace(0, w, num_divs + 1).astype(int)
    
    source_display = original_img.copy()
    grid_color = (200, 200, 200)
    for y in y_bounds: cv2.line(source_display, (0, y), (w, y), grid_color, 1)
    for x in x_bounds: cv2.line(source_display, (x, 0), (x, h), grid_color, 1)

    grid_blank = np.zeros((h, w, 3), dtype=np.uint8)
    for y in y_bounds: cv2.line(grid_blank, (0, y), (w, y), (100, 100, 100), 1)
    for x in x_bounds: cv2.line(grid_blank, (x, 0), (x, h), (100, 100, 100), 1)
    
    warped_grid = cv2.remap(grid_blank, map_x, map_y, cv2.INTER_LINEAR)

    target_content = np.zeros_like(original_img)
    canvas = np.zeros((h, w * 2, 3), dtype=np.uint8)
    canvas[:, :w] = source_display

    win_name = "Droste Math Visualizer"

    for r in range(num_divs):
        for c in range(num_divs):
            y1, y2, x1, x2 = y_bounds[r], y_bounds[r+1], x_bounds[c], x_bounds[c+1]
            
            full_mask = (map_x >= x1) & (map_x < x2) & (map_y >= y1) & (map_y < y2)
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(full_mask.astype(np.uint8)*255)
            
            if num_labels <= 1: continue 

            idx = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
            s = stats[idx]
            tx, ty, tw, th = s[cv2.CC_STAT_LEFT], s[cv2.CC_STAT_TOP], s[cv2.CC_STAT_WIDTH], s[cv2.CC_STAT_HEIGHT]
            
            curvy_piece = perfect_result[ty:ty+th, tx:tx+tw]
            curvy_mask = (labels[ty:ty+th, tx:tx+tw] == idx).astype(np.uint8) * 255
            square_piece = original_img[y1:y2, x1:x2]

            start_center = np.array([y1 + (y2-y1)/2, x1 + (x2-x1)/2])
            end_center = np.array([centroids[idx][1], centroids[idx][0] + w])
            
            for i in range(fly_steps + 1):
                t = ease_in_out_quad(i / fly_steps)
                
                curr_y, curr_x = ((1 - t) * start_center + t * end_center).astype(int)
                
                cw = int((x2 - x1) * (1 - t) + tw * t)
                ch = int((y2 - y1) * (1 - t) + th * t)
                if ch < 2 or cw < 2: continue

                morphed_tex = cv2.addWeighted(cv2.resize(square_piece, (cw, ch)), 1-t, 
                                              cv2.resize(curvy_piece, (cw, ch)), t, 0)
                m_res = cv2.resize(curvy_mask, (cw, ch), interpolation=cv2.INTER_NEAREST)

                canvas[:, w:] = cv2.addWeighted(target_content, 1.0, warped_grid, 0.5, 0)
                
                y_s, x_s = curr_y - ch//2, curr_x - cw//2
                if 0 <= y_s < h - ch and 0 <= x_s < w*2 - cw:
                    roi = canvas[y_s:y_s+ch, x_s:x_s+cw]

                    mask_inv = cv2.bitwise_not(m_res)
                    bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
                    fg = cv2.bitwise_and(morphed_tex, morphed_tex, mask=m_res)
                    canvas[y_s:y_s+ch, x_s:x_s+cw] = cv2.add(bg, fg)

                display_canvas = canvas.copy()

                cv2.imshow(win_name, display_canvas)
                if cv2.waitKey(step_delay) != -1: 
                    return perfect_result

            target_content[full_mask] = perfect_result[full_mask]

            source_display[y1:y2, x1:x2] = source_display[y1:y2, x1:x2] // 4
            canvas[:, :w] = source_display

    cv2.putText(canvas, "Finished! Press ANY KEY to return to menu", (30, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.imshow(win_name, canvas)
    cv2.waitKey(0)

    return perfect_result

def animate_droste_steps(img, m1, m2, m3, zoom_provider, frames_per_step=60):
    h, w = img.shape[:2]
    
    grid_y, grid_x = np.indices((h, w), dtype=np.float32)
    m0 = (grid_x, grid_y)
    
    stages = [m0, m1, m2, m3]
    stage_names = ["Original", "Log Space", "Rotated Log Space", "Final Escher Droste"]

    window_name = "Droste Math Visualizer"

    for i in range(len(stages) - 1):
        for f in range(frames_per_step):
            t = (1.0 - np.cos((f / frames_per_step) * np.pi)) / 2.0 
            
            mx = ((1.0 - t) * stages[i][0] + t * stages[i+1][0]).astype(np.float32)
            my = ((1.0 - t) * stages[i][1] + t * stages[i+1][1]).astype(np.float32)
            
            frame = cv2.remap(img, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)
            
            cv2.putText(frame, f"{stage_names[i+1]}", (30, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2, cv2.LINE_AA)
            cv2.imshow(window_name, frame)
            
            if cv2.waitKey(1) != -1: 
                return 

    f_idx = 0
    while True:
        t = (f_idx % frames_per_step) / float(frames_per_step)
        
        mx, my = zoom_provider(t)
        
        frame = cv2.remap(img, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        
        cv2.putText(frame, "Finished! Press ANY KEY to return to menu", (30, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0, 0), 2, cv2.LINE_AA)
        cv2.imshow(window_name, frame)
        
        f_idx += 1
        
        if cv2.waitKey(1) != -1: 
            break
            