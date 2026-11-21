import cv2, os

os.makedirs("assets/characters/demo_scenes", exist_ok=True)

# sec_10: Mother shouting, Bob listening, Friend listening
cv2.imwrite("assets/characters/demo_scenes/mother_speaking.png", cv2.imread("output/demo_frames/sec_10.png"))

# sec_14: Mother worried listening, Bob listening, Friend sly smirk
cv2.imwrite("assets/characters/demo_scenes/mother_listening.png", cv2.imread("output/demo_frames/sec_14.png"))

# sec_18: Friend talking with gesture to Mother, Bob listening, Mother listening
cv2.imwrite("assets/characters/demo_scenes/friend_speaking.png", cv2.imread("output/demo_frames/sec_18.png"))

# sec_20: Friend talking with mouth open, Bob attentive
cv2.imwrite("assets/characters/demo_scenes/friend_gesture.png", cv2.imread("output/demo_frames/sec_20.png"))

# sec_22: Mother talking back, Bob listening
cv2.imwrite("assets/characters/demo_scenes/mother_reassure.png", cv2.imread("output/demo_frames/sec_22.png"))

# sec_24: Bob speaking/laughing with wide mouth ("हो माय!"), Mother listening, Friend proud eyes closed
cv2.imwrite("assets/characters/demo_scenes/bob_speaking.png", cv2.imread("output/demo_frames/sec_24.png"))

# sec_28: Bob laughing happy
cv2.imwrite("assets/characters/demo_scenes/bob_laughing.png", cv2.imread("output/demo_frames/sec_28.png"))

print("Extracted all authentic demo scene states successfully!")
