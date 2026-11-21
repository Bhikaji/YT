import cv2
import numpy as np

img10 = cv2.imread("output/demo_frames/sec_10.png")
img16 = cv2.imread("output/demo_frames/sec_16.png")
img20 = cv2.imread("output/demo_frames/sec_20.png")
img24 = cv2.imread("output/demo_frames/sec_24.png")

# Mother box in sec_10: x: 620 to 770, y: 340 to 630
mother_crop10 = img10[340:635, 620:770]
cv2.imwrite("output/test_mother_crop10.png", mother_crop10)

# Bob box in sec_10: x: 780 to 900, y: 350 to 620
# Let's inspect where Bob is: x from 750 to 900
bob_crop10 = img10[350:620, 750:900]
cv2.imwrite("output/test_bob_crop10.png", bob_crop10)

# Friend box in sec_10: x: 880 to 1030, y: 280 to 520
friend_crop10 = img10[280:520, 880:1030]
cv2.imwrite("output/test_friend_crop10.png", friend_crop10)

print("Saved test crops for Mother, Bob, Friend.")
