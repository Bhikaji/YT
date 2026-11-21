import cv2, os

os.makedirs("assets/characters/demo_patches", exist_ok=True)

im10 = cv2.imread("output/demo_frames/sec_10.png")
im14 = cv2.imread("output/demo_frames/sec_14.png")
im20 = cv2.imread("output/demo_frames/sec_20.png")
im24 = cv2.imread("output/demo_frames/sec_24.png")

# 1. Mother mouth (in im10 speaking vs im14 listening)
# Mother head is around (620..760, 340..480). Mouth is roughly (670..735, 430..475)
m_open = im10[430:475, 670:735]
m_closed = im14[430:475, 670:735]
cv2.imwrite("assets/characters/demo_patches/mother_mouth_open.png", m_open)
cv2.imwrite("assets/characters/demo_patches/mother_mouth_closed.png", m_closed)

# 2. Bob mouth (in im24 speaking vs im14 listening)
# Bob head is around (750..900, 350..480). Mouth is roughly (800..865, 435..475)
b_open = im24[435:475, 800:865]
b_closed = im14[435:475, 800:865]
cv2.imwrite("assets/characters/demo_patches/bob_mouth_open.png", b_open)
cv2.imwrite("assets/characters/demo_patches/bob_mouth_closed.png", b_closed)

# 3. Friend mouth (in im20 speaking vs im14 listening)
# Friend head is around (880..1030, 270..420). Mouth is roughly (920..980, 350..390)
f_open = im20[350:390, 920:980]
f_closed = im14[350:390, 920:980]
cv2.imwrite("assets/characters/demo_patches/friend_mouth_open.png", f_open)
cv2.imwrite("assets/characters/demo_patches/friend_mouth_closed.png", f_closed)

print("Saved mouth patches successfully!")
