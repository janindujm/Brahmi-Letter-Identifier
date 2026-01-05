import tkinter as tk
from tkinter import messagebox
import os
import time
import cv2
import numpy as np
import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn import metrics
import joblib
from PIL import ImageGrab  # Use PIL for capturing canvas area

# ----------------- Window -----------------
window = tk.Tk()
window.title("Brahmi Letter Recognition")
window.geometry("800x600")  # Bigger window for canvas
window.state("zoomed")
# ----------------- Labels and Entry -----------------
l1 = tk.Label(window, text="Brahmi Letter", font=('Algerian', 20))
l1.place(x=5, y=0)

t1 = tk.Entry(window, width=20, border=5)
t1.place(x=220, y=5)

# ----------------- Drawing Canvas -----------------
canvas_width = 400
canvas_height = 400
canvas_x = 50
canvas_y = 50

canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="black")
canvas.place(x=canvas_x, y=canvas_y)

# Variables to track drawing
last_x, last_y = None, None

def activate_paint(event):
    global last_x, last_y
    last_x, last_y = event.x, event.y

def paint(event):
    global last_x, last_y
    x, y = event.x, event.y
    if last_x and last_y:
        canvas.create_line(last_x, last_y, x, y, fill="white", width=8, capstyle=tk.ROUND, smooth=True)
    last_x, last_y = x, y

def reset(event):
    global last_x, last_y
    last_x, last_y = None, None

canvas.bind("<Button-1>", activate_paint)
canvas.bind("<B1-Motion>", paint)
canvas.bind("<ButtonRelease-1>", reset)

# ----------------- Clear Canvas -----------------
def clear_canvas():
    canvas.delete("all")

b_clear = tk.Button(window, text="Clear Canvas", font=('Algerian', 15), bg="red", fg="white", command=clear_canvas)
b_clear.place(x=500, y=100)

# ----------------- Capture Canvas -----------------
def screen_capture():
    #letter_label = t1.get().strip()
    #if not letter_label:
    #    messagebox.showerror("Error", "Please enter a Brahmi letter first!")
    #    return


    images_folder = os.path.join("captured_images", "ka")
    os.makedirs(images_folder, exist_ok=True)

    #messagebox.showinfo("Info", "You have 3 seconds before capture. Draw your letter!")
    window.update()
    #time.sleep(3)

    # Get canvas coordinates on screen
    # Get exact canvas coordinates on screen


    bbox=(66, 94, 560, 587)
    im = ImageGrab.grab(bbox=bbox)
    count = len(os.listdir(images_folder))
    im.save(os.path.join(images_folder, f"{count}.png"))
    #messagebox.showinfo("Result", f"Image saved as {count}.png")
    clear_canvas()

b1 = tk.Button(window, text="Capture Drawing", font=('Algerian', 15), bg="orange", fg="black", command=screen_capture)
b1.place(x=500, y=50)


# ----------------- Live Prediction -----------------
def prediction():
    model_path = os.path.join("model", "digit_recognizer")
    if not os.path.exists(model_path):
        messagebox.showerror("Error", "Model not found! Train first.")
        return

    classifier = joblib.load(model_path)


    # Get exact canvas coordinates on screen
    x = canvas.winfo_rootx() + 65 
    y = canvas.winfo_rooty()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()

    bbox=(66, 94, 560, 587)
    im = ImageGrab.grab(bbox=bbox)
    im.save("img.png")
    im_cv = cv2.imread("img.png", cv2.IMREAD_GRAYSCALE)
    im_cv = cv2.GaussianBlur(im_cv, (15, 15), 0)
    roi = cv2.resize(im_cv, (28, 28), interpolation=cv2.INTER_AREA)
    binary_pixels = np.where(roi > 100, 1, 0)
    X_input = binary_pixels.flatten().tolist()
    pred = classifier.predict([X_input])[0]

    messagebox.showinfo("Prediction", f"Predicted Letter: {pred}")
    clear_canvas()

b4 = tk.Button(window, text="Predict Letter", font=('Algerian', 15), bg="white", fg="red", command=prediction)
b4.place(x=500, y=250)

window.mainloop()
