import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
import os
import re
import camera_gui_library as camera  # Import the camera module
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
#import polhemus_interface as pol
#import leapmotion_interface as leapm
#import vive_data_tracker as vive
import zipfile
import time
#import psutil


# Global variables for tracker and camera processes
STARTED = False
start_time = None
polhemus_thread = None
leapmotion_thread = None
vive_thread = None
selected_camera_index = None

# Create the main window
window = tk.Tk()
window.title("Tracker and Camera Interface")
window.resizable(False, False)

# Variables for tracker checkboxes
POLHEMUS = tk.BooleanVar()
LEAPMOTION = tk.BooleanVar()
VIVE = tk.BooleanVar()

# Polling rate input
label = tk.Label(window, text="Polling Rate (Hz):")
label.grid(row=0, column=0)
hz_field = tk.Entry(window)
hz_field.grid(row=0, column=1)

# Stopwatch
stopwatch_label = tk.Label(window, text="00:00:00.000")
stopwatch_label.grid(row=0, column=3)

# Dropdown for camera selection
camera_var = tk.StringVar(value="Select a camera")
camera_dropdown = ttk.Combobox(window, textvariable=camera_var, values=[], state="readonly")
camera_dropdown.grid(row=4, column=0)

# Button for camera preview
preview_button = tk.Button(window, text="Preview Camera", command=lambda: camera.preview_camera(selected_camera_index))
preview_button.grid(row=4, column=1)

def start_button_wrapper():
    try:
        os.remove("polhemus_output.csv")
    except:
        pass
    try:
        os.remove("leapmotion_output.csv")
    except:
        pass
    try:
        pattern = re.compile(r'.*_data\..*')
        for file in os.listdir('./'):
            if pattern.match(file):
                os.remove(file)
    except:
        pass

    # Check if a valid polling rate is entered
    try:
        hz = int(hz_field.get())
        if hz <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Polling rate error", "Please enter a valid positive integer for the polling rate.")
        return  # If invalid polling rate, stop further execution

    # Start camera recording along with trackers only if polling rate is valid
    camera.start_camera_recording(selected_camera_index, camera_var, window)  # Start camera recording
    begin_tracking()          # Start tracker processes

    toggle_stop()


def stop_button_wrapper():
    stop_output()             # Stop tracking process
    camera.stop_camera_recording()    # Stop camera recording
    toggle_stop()

def toggle_stop():
    if STARTED:
        stop_button.config(state="normal")
        start_button.config(state="disabled")
    else:
        stop_button.config(state="disabled")
        start_button.config(state="normal")

def stop_output():
    global STARTED
    if POLHEMUS.get():
        if polhemus_thread is not None:
            polhemus_thread.join()  # Wait for the thread to finish
    if LEAPMOTION.get():
        print("LeapMotion placeholder")
    if VIVE.get():
        print("Vive placeholder")
    STARTED = False

def begin_tracking():
    try:
        hz = int(hz_field.get())
    except ValueError:
        messagebox.showerror("Polling rate error", "Please enter a valid integer for the polling rate.")
        return

    global STARTED, start_time
    if not STARTED:
        STARTED = True
        start_time = time.time()
        stopwatch_label.config(text="00:00:00")
        start_stopwatch()
        if POLHEMUS.get():
            global polhemus_thread
            polhemus_thread.start()
        if LEAPMOTION.get():
            global leapmotion_thread
            leapmotion_thread.start()
        if VIVE.get():
            global vive_thread
            vive_thread.start()

def start_stopwatch():
    global STARTED
    if STARTED:
        elapsed_time = time.time() - start_time
        milliseconds = int((elapsed_time * 1000) % 1000)
        seconds = int(elapsed_time) % 60
        minutes = (int(elapsed_time) // 60) % 60
        hours = (int(elapsed_time) // 3600) % 24
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"
        stopwatch_label.config(text=time_str)
        window.after(10, start_stopwatch)

def select_camera(event):
    global selected_camera_index
    selected_camera_index = int(camera_var.get())
    print(f"Camera {selected_camera_index} selected")

camera_dropdown.bind("<<ComboboxSelected>>", select_camera)

# UI Buttons for trackers
start_button = tk.Button(window, text="Start", command=start_button_wrapper)
start_button.grid(row=1, column=3, sticky="ew")

stop_button = tk.Button(window, text="Stop", command=stop_button_wrapper, state="disabled")
stop_button.grid(row=2, column=3, sticky="ew")

file_picker_button = tk.Button(window, text="Save zip to...", command=lambda: filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP Files", "*.zip")]))
file_picker_button.grid(row=3, column=3)

# Start the main event loop and initialize the valid cameras
if __name__ == "__main__":
    try:
        os.remove("polhemus_output.csv")
    except:
        pass
    try:
        os.remove("leapmotion_output.csv")
    except:
        pass
    try:
        pattern = re.compile(r'.*_data\..*')
        for file in os.listdir('./'):
            if pattern.match(file):
                os.remove(file)
    except:
        pass
    valid_cameras = camera.find_valid_cameras()
    camera_dropdown["values"] = valid_cameras  # Populate the camera dropdown
    window.mainloop()
