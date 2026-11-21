import cv2
import numpy as np

img = cv2.imread("output/demo_frames/sec_10.png")
h, w = img.shape[:2]

# Character bounding box is roughly x: 570 to 830, y: 320 to 650
mask = np.zeros((h, w), dtype=np.uint8)

# Mother region
mask[340:650, 580:670] = 255
# Bob region
mask[480:650, 660:735] = 255
# Friend region
mask[370:580, 725:825] = 255

# Refine mask: only inpaint non-background pixels inside this bounding box
# Or inpaint with cv2
clean = cv2.inpaint(img, mask, inpaintRadius=7, flags=cv2.INPAINT_TELEA)

cv2.imwrite("output/test_clean_bus_plate.png", clean)
print("Saved output/test_clean_bus_plate.png")
