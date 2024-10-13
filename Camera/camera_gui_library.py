import cv2
import datetime
import tkinter as tk
from tkinter import messagebox

# Global variables for camera and recording
cap = None
out = None
is_recording = False
selected_camera_index = None

def initialize_camera(camera_index):
    global cap
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        messagebox.showerror("Error", f"Could not open camera {camera_index}")
        return False
    return True

def start_camera_recording(selected_camera_index, camera_var, window):
    global out, is_recording
    if selected_camera_index is None:
        messagebox.showerror("Error", "Please select a camera first.")
        return
    if not initialize_camera(selected_camera_index):
        return

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output_{timestamp}.mov"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    is_recording = True
    process_frame(window)

def stop_camera_recording():
    global out, is_recording
    if is_recording:
        out.release()
        is_recording = False
        cap.release()
        cv2.destroyAllWindows()

def preview_camera(selected_camera_index):
    global cap
    if selected_camera_index is None:
        messagebox.showerror("Error", "Please select a camera first.")
        return
    cap = cv2.VideoCapture(selected_camera_index)
    if not cap.isOpened():
        messagebox.showerror("Error", f"Could not open camera {selected_camera_index}")
        return

    start_time = datetime.datetime.now().timestamp()
    while datetime.datetime.now().timestamp() - start_time < 3:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow(f"Preview of Camera {selected_camera_index}", frame)
        cv2.setWindowProperty(f"Preview of Camera {selected_camera_index}", cv2.WND_PROP_TOPMOST, 1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def process_frame(window):
    global out, is_recording
    if is_recording:
        ret, frame = cap.read()
        if not ret:
            stop_camera_recording()
            return
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.imshow('Camera Feed', frame)
        out.write(frame)
        window.after(10, lambda: process_frame(window))

def find_valid_cameras():
    available_cameras = list(range(10))
    valid_cameras = []
    for i in available_cameras:
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            valid_cameras.append(i)
        cap.release()
    return valid_cameras
