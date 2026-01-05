import pyscreenshot as ImageGrab
import time

images_folder = "Screenshots/ga/"
bbox = (523,320,1400,872)  # Define the bounding box (left_x, top_y, right_x, bottom_y)

for i in range(0,80):
    time.sleep(3)
    img = ImageGrab.grab(bbox=bbox)
    img.save(images_folder + f"screenshot_{i+20}.png")
    print(f"Screenshot {i+20} saved successfully")

print("All screenshots captured successfully")