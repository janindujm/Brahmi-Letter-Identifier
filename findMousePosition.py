import pyautogui
import time

print("Move mouse to TOP-LEFT corner and wait 5 seconds...")
time.sleep(5)
x1, y1 = pyautogui.position()
print("Top-left:", x1, y1)

print("Move mouse to BOTTOM-RIGHT corner and wait 5 seconds...")
time.sleep(5)
x2, y2 = pyautogui.position()
print("Bottom-right:", x2, y2)
