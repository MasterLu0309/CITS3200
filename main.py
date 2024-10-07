import tkinter as tk  
from tkinter import filedialog, ttk, messagebox  
import threading  
import polhemus_interface as pol  
import leapmotion_interface as leapm  
import camera_interface as cam  
import os  
import zipfile 
import time  
import psutil

# Global variables
STARTED = False
CAMERA_STARTED = False
start_time = None
polhemus_thread = None
leapmotion_thread = None
camera_thread = None

# Create the main window
window = tk.Tk() 
window.title("Tracker Interface") 
window.resizable(False, False) 

# Create Boolean variables for tracker options
POLHEMUS = tk.BooleanVar()
LEAPMOTION = tk.BooleanVar()
VIVE = tk.BooleanVar()
CAMERA = tk.BooleanVar()  

# Add Label for Tracker Polling Rate
label = tk.Label(window, text="Polling Rate (Hz):")
label.grid(row=0, column=0)

# Add Text Entry Field for Tracker Polling Rate
hz_field = tk.Entry(window)
hz_field.grid(row=0, column=1)

# Add Label for Camera Polling Rate
camera_label = tk.Label(window, text="Camera Polling Rate (Hz):")
camera_label.grid(row=1, column=0)

# Add Text Entry Field for Camera Polling Rate
camera_hz_field = tk.Entry(window)
camera_hz_field.grid(row=1, column=1)

# Add Checkbox for Camera
camera_checkbox = tk.Checkbutton(window, text="Camera", variable=CAMERA) 
camera_checkbox.grid(row=2, column=0)  

# Add Stopwatch Label
stopwatch_label = tk.Label(window, text="00:00:00.000")
stopwatch_label.grid(row=0, column=3)

# Function to check if the Leapmotion service is running
def check_leapmotion_service():
    try:
        service = psutil.win_service_get("UltraleapTracking")
        status = service.status()
        return status == "running"
    except:
        return False

def toggle_leapmotion():
    """Enable or disable Leapmotion mode based on service status."""
    if LEAPMOTION.get():  
        if not check_leapmotion_service():  
            messagebox.showerror("Ultraleap Service Error", "Please ensure the Ultraleap Tracking service is running.", parent=window)
            LEAPMOTION.set(False)  
            return
        leapmotion_mode.config(state="readonly") 
    else:
        leapmotion_mode.config(state="disabled")  

def start_button_wrapper():
    """Wrapper function to start tracking."""
    begin_tracking()  
    if CAMERA.get(): 
        start_camera()  
    toggle_stop()

def stop_button_wrapper():
    """Wrapper function to stop tracking."""
    stop_output()  
    stop_camera() 
    toggle_stop()

def toggle_stop():
    """Toggle the state of Start and Stop buttons."""
    if STARTED:
        stop_button.config(state="normal")
        start_button.config(state="disabled")  
    else:
        stop_button.config(state="disabled") 
        start_button.config(state="normal")

# Add checkboxes for tracker selection
polhemus_checkbox = tk.Checkbutton(window, text="Polhemus", variable=POLHEMUS)  
polhemus_checkbox.grid(row=3, column=0, sticky="w") 
leapmotion_checkbox = tk.Checkbutton(window, text="Leapmotion", variable=LEAPMOTION, command=toggle_leapmotion) 
leapmotion_checkbox.grid(row=4, column=0, sticky="w") 
vive_checkbox = tk.Checkbutton(window, text="Vive", variable=VIVE)
vive_checkbox.grid(row=5, column=0, sticky="w")

# Tkinter combobox (dropdown) for Leapmotion modes
options = ["Desktop", "Head Mounted", "Screentop"]  
leapmotion_mode = ttk.Combobox(window, values=options, state="disabled")  
leapmotion_mode.set("Leapmotion mode...") 
leapmotion_mode.grid(row=4, column=1)

def stop_output():
    """Stop output for tracking devices."""
    global STARTED
    if POLHEMUS.get(): 
        pol.another = False  
    if LEAPMOTION.get(): 
        leapm.another = False
        leapm.connection.disconnect()  
    global CAMERA_STARTED
    if CAMERA_STARTED: 
        stop_camera()  
    STARTED = False 

def start_output():
    """Start output for tracking devices."""
    global STARTED
    # Check if hz is valid
    try:
        hz = int(hz_field.get())  
    except:
        STARTED = False
        raise ValueError("Please enter a valid integer for the frequency.")  

    pol.output_data(hz) 

def stop_camera():
    """Stop the camera."""
    global CAMERA_STARTED
    CAMERA_STARTED = False  

def start_camera():
    """Start the camera with specified polling rate."""
    global camera_thread, CAMERA_STARTED
    try:
        camera_hz = int(camera_hz_field.get()) 
    except ValueError:
        messagebox.showerror("Camera Polling Rate Error", "Please enter a valid integer for the camera polling rate.", parent=window)
        return

    if camera_hz <= 0:
        messagebox.showerror("Camera Polling Rate Error", "Polling rate must be a positive integer.", parent=window)
        return

    CAMERA_STARTED = True 
    camera_thread = threading.Thread(target=cam.start_camera, args=(1/camera_hz,), daemon=True)  
    camera_thread.start() 

def hz_messagebox():
    """Show error message for invalid polling rate."""
    messagebox.showerror("Polling rate error", "Please enter a valid integer for the polling rate.", parent=window)

def begin_tracking():
    """Begin the tracking process."""
    try:
        _ = int(hz_field.get()) 
    except:
        hz_messagebox()  
        return
    if int(hz_field.get()) <= 0: 
        hz_messagebox() 
        return
    else:
        if LEAPMOTION.get() and (leapmotion_mode.get() not in ["Desktop", "Head Mounted", "Screentop"]):
            raise ValueError("Please select a valid mode for Leapmotion.")
        global STARTED, start_time
        if not STARTED:  
            STARTED = True 
            start_time = time.time()
            stopwatch_label.config(text="00:00:00") 
            start_stopwatch()  
            if POLHEMUS.get():  
                polhemus_thread = threading.Thread(target=start_output, daemon=True) 
                polhemus_thread.start() 
            if LEAPMOTION.get(): 
                leapm.another = True  
                leapm.SELECTED_MODE = leapm.tracking_modes[leapmotion_mode.get()]  
                leapmotion_thread = threading.Thread(target=leapm.initialise_leapmotion, daemon=True, args=(int(hz_field.get()),)) 
                leapmotion_thread.start() 
        else:
            print("Already started.")  

def open_file_picker():
    """Open a file picker dialog to save the output files."""
    if not STARTED:  
        file_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP Files", "*.zip")])  
        print(file_path) 
        zip_files(["polhemus_output.csv", "leapmotion_output.csv"], file_path) 
    else:
        print("Cannot save file while tracking.") 

def start_stopwatch():
    """Update and display the stopwatch for elapsed time."""
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

def zip_files(files: list[str], zip_name: str):
    """Zip specified files into a single zip file."""
    with zipfile.ZipFile(zip_name, "w") as zipf: 
        for file in files:
            try:
                zipf.write(file, os.path.basename(file)) 
            except:
                # File does not exist (that tracker must not have been used)
                pass

# Add Button 1 for Start
start_button = tk.Button(window, text="Start", command=start_button_wrapper)
start_button.grid(row=5, column=3, sticky="ew") 

# Add Button 2 for Stop
stop_button = tk.Button(window, text="Stop", command=stop_button_wrapper, state="disabled")  
stop_button.grid(row=6, column=3, sticky="ew")  

# File picker
file_picker_button = tk.Button(window, text="Save zip to...", command=open_file_picker) 
file_picker_button.grid(row=7, column=3) 

# Start the main event loop
if __name__ == "__main__":
    try:
        os.remove("polhemus_output.csv") 
    except:
        pass
    try:
        os.remove("leapmotion_output.csv")
    except:
        pass
    pol.initialise_polhemus(1)  
    window.mainloop() 
