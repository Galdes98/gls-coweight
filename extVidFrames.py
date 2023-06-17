import cv2
import tkinter as tk
from tkinter import filedialog

# Prompt user to select a video file
root = tk.Tk()
root.withdraw()
video_path = filedialog.askopenfilename()

# Prompt user to select a destination directory
folder_path = filedialog.askdirectory()

# Load video file
cap = cv2.VideoCapture(video_path)

# Check if video file opened successfully
if not cap.isOpened():
    print("Error opening video file")
    exit()

# Initialize frame count and image number
frame_count = 0
img_num = 0

# Loop through video frames
while cap.isOpened():
    # Read a frame
    ret, frame = cap.read()

    # Check if frame read successfully
    if not ret:
        break

    # Increment frame count
    frame_count += 1

    # Save frame as image in selected folder
    cv2.imwrite(f"{folder_path}/image{img_num:04d}.jpg", frame)

    # Increment image number
    img_num += 1

# Release video file and close all windows
cap.release()
cv2.destroyAllWindows()