import cv2
import numpy as np

def generate_perfect_test_droste(size=1024, S=4):
    img = np.full((size, size, 3), 40, dtype=np.uint8)
    
    grid_spacing = size // 16
    for i in range(0, size, grid_spacing):
        cv2.line(img, (i, 0), (i, size), (100, 100, 100), 1)
        cv2.line(img, (0, i), (size, i), (100, 100, 100), 1)

    cv2.line(img, (0, 0), (size, size), (255, 255, 0), 2)     
    cv2.line(img, (size, 0), (0, size), (255, 0, 255), 2)       
    
    thickness = 15
    cv2.rectangle(img, (0, 0), (size, thickness), (0, 0, 255), -1)
    cv2.putText(img, "TOP", (size//2 - 40, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
    
    cv2.rectangle(img, (0, size - thickness), (size, size), (255, 0, 0), -1)
    cv2.putText(img, "BOTTOM", (size//2 - 70, size - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)
    
    cv2.rectangle(img, (0, 0), (thickness, size), (0, 255, 0), -1)
    
    cv2.rectangle(img, (size - thickness, 0), (size, size), (0, 255, 255), -1)

    c = size // 2
    cv2.line(img, (c - 50, c), (c + 50, c), (255, 255, 255), 2)
    cv2.line(img, (c, c - 50), (c, c + 50), (255, 255, 255), 2)
    cv2.circle(img, (c, c), 10, (255, 255, 255), -1)

    inner_size = int(size / S)
    start = (size - inner_size) // 2
    end = start + inner_size
    
    inner_version = cv2.resize(img, (inner_size, inner_size))
    
    img[start:end, start:end] = inner_version
    
    cv2.rectangle(img, (start, start), (end, end), (255, 255, 255), 3)
    
    cv2.putText(img, "SEAM", (start, start - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    filename = f"perfect_droste_test_{S}.png"
    cv2.imwrite(filename, img)
    print(f"Test image '{filename}' saved!")
    print(f"Size: {size}x{size}")
    print(f"Center: ({c}, {c})")
    print(f"Zoom Factor (S): {S}")
    print(f"Inner Width: {inner_size}px (Bounds: {start} to {end})")

if __name__ == "__main__":
    generate_perfect_test_droste(size=1024, S=64)