import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math

base_img = cv2.imread("assets/characters/demo_scenes/mother_listening.png")

# Load mouth patches
m_open = cv2.imread("assets/characters/demo_patches/mother_mouth_open.png")
m_closed = cv2.imread("assets/characters/demo_patches/mother_mouth_closed.png")

b_open = cv2.imread("assets/characters/demo_patches/bob_mouth_open.png")
b_closed = cv2.imread("assets/characters/demo_patches/bob_mouth_closed.png")

f_open = cv2.imread("assets/characters/demo_patches/friend_mouth_open.png")
f_closed = cv2.imread("assets/characters/demo_patches/friend_mouth_closed.png")

# Friend speaking crop (body & arm from sec_18)
im18 = cv2.imread("output/demo_frames/sec_18.png")
friend_spk_body = im18[270:550, 880:1030]

def render_puppet_frame(speaker: str, mouth_is_open: bool, is_punchline: bool = False):
    frame = base_img.copy()
    
    if is_punchline:
        laugh = cv2.imread("assets/characters/demo_scenes/bob_laughing.png")
        return laugh
        
    if "mother" in speaker.lower():
        patch = m_open if mouth_is_open else m_closed
        frame[430:475, 670:735] = patch
    elif "bob" in speaker.lower():
        patch = b_open if mouth_is_open else b_closed
        frame[435:475, 800:865] = patch
    elif "friend" in speaker.lower() or "prof" in speaker.lower():
        # Place friend speaking body
        frame[270:550, 880:1030] = friend_spk_body
        patch = f_open if mouth_is_open else f_closed
        frame[350:390, 920:980] = patch
        
    return frame

# Generate test frames
cv2.imwrite("output/test_sync_bob_open.png", render_puppet_frame("bob", True))
cv2.imwrite("output/test_sync_bob_closed.png", render_puppet_frame("bob", False))

cv2.imwrite("output/test_sync_mother_open.png", render_puppet_frame("mother", True))
cv2.imwrite("output/test_sync_mother_closed.png", render_puppet_frame("mother", False))

cv2.imwrite("output/test_sync_friend_open.png", render_puppet_frame("friend", True))
cv2.imwrite("output/test_sync_friend_closed.png", render_puppet_frame("friend", False))

print("Rendered all test sync frames successfully!")
