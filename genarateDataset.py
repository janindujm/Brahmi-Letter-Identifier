# Generate dataset
import cv2
import csv
import glob
import numpy as np
import os

# CSV file path
csv_file = 'dataset.csv'

# Resize images to 28x28 (you can change if needed)
IMG_SIZE = 28

# Remove existing CSV if exists (optional, to start fresh)
if os.path.exists(csv_file):
    os.remove(csv_file)

# --------- Write CSV header ---------
header = ["label"]
for i in range(IMG_SIZE * IMG_SIZE):
    header.append(f"pixel{i}")

with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

# --------- Your labels ---------
labels = ["ka", "ga", "ki" , "ha", "pa"]  # list of your labels

# --------- Process images ---------
for label in labels:
    dir_list = glob.glob(f"Screenshots/{label}/*.png")

    for img_path in dir_list:
        # Read image
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Optional: blur to remove noise
        gray = cv2.GaussianBlur(gray, (15, 15), 0)

        # Resize to 28x28
        roi = cv2.resize(gray, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_AREA)

        # Convert pixels to 0/1
        binary_pixels = np.where(roi > 100, 1, 0)

        # Flatten to 1D array
        flat_pixels = binary_pixels.flatten()

        # Combine label + pixels
        data_row = [label] + flat_pixels.tolist()

        # Append row to CSV
        with open(csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data_row)

print("Dataset CSV created successfully!")
