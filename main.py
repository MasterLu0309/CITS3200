import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
import polhemus_interface as pol
import leapmotion_interface as leapm
import vive_data_tracker as vive
import camera_gui_library as camera
import os
import zipfile
import time
import re
import psutil


# Global variable to keep track of whether tracking is actively underway.
STARTED = False

# Global variable to keep track of the start time of tracking.
start_time = None

# Global variables containing the thread each tracker's process will run on.
polhemus_thread = None
leapmotion_thread = None
vive_thread = None
camera_thread = None
selected_camera_index = None

# Create the main window
window = tk.Tk()
window.title("Tracker Interface")
window.resizable(False, False)

# Variables correspond to the UI checkboxes for respective trackers.
POLHEMUS = tk.BooleanVar()
LEAPMOTION = tk.BooleanVar()
VIVE = tk.BooleanVar()
USE_CAMERA = tk.BooleanVar()

# POLLING RATE
label = tk.Label(window, text="Polling Rate (Hz):")
label.grid(row=0, column=0)
hz_field = tk.Entry(window)
hz_field.grid(row=0, column=1)

# STOPWATCH
stopwatch_label = tk.Label(window, text="00:00:00.000")
stopwatch_label.grid(row=0, column=3)

# Add Camera checkbox
camera_checkbox = tk.Checkbutton(window, text="Camera", variable=USE_CAMERA)
camera_checkbox.grid(row=4, column=0, sticky="w")

#Dropdown for camera selection
camera_var = tk.StringVar(value="Select a camera")
camera_dropdown = ttk.Combobox(window, textvariable=camera_var, values=[], state="readonly")
camera_dropdown.grid(row=4, column=1)  

# Button for camera preview
preview_button = tk.Button(window, text="Preview Camera", command=lambda: camera.preview_camera(selected_camera_index))
preview_button.grid(row=4, column=2) 




def check_leapmotion_service():
    '''
    Test to see if the Ultraleap Tracking service is running on the system.
    '''
    try:
        service = psutil.win_service_get("UltraleapTracking")
        status = service.status()
        return status == "running"
    except:
        return False

def toggle_leapmotion():
    '''
    Underlying function when checking/unchecking Leapmotion checkbox.
    '''
    if LEAPMOTION.get():
        if not check_leapmotion_service():
            messagebox.showerror("Ultraleap Service Error", "Please ensure the Ultraleap Tracking service is running.", parent=window)
            LEAPMOTION.set(False)
            return
        leapmotion_mode.config(state="readonly")
    else:
        leapmotion_mode.config(state="disabled")

# Underlying functions for start and stop buttons
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

    #Check if valid polling rate is entered
    try:
        hz = int(hz_field.get())
        if hz <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Polling rate error", "Please enter a valid positive integer for the polling rate.")
        return  # If invalid polling rate, stop further execution
    
    #Check if camera is selected and check if valid camera selected
    if USE_CAMERA.get():
        if  selected_camera_index is None:
            messagebox.showerror("Camera Selection Error", "Please select a camera before starting.")
            return  # If no camera selected, stop further execution
    
    #Start trackers and camera if selected
    begin_tracking()
    if USE_CAMERA.get():
        camera.start_camera_recording(selected_camera_index, camera_var, window)# Start camera recording
    toggle_stop()

def stop_button_wrapper():
    stop_output() #stops all tracker
    if USE_CAMERA.get():
        camera.stop_camera_recording() #Stop camera recording
    toggle_stop()

def toggle_stop():
    if STARTED:
        stop_button.config(state="normal")
        start_button.config(state="disabled")
    else:
        stop_button.config(state="disabled")
        start_button.config(state="normal")

# Render checkboxes for each tracker
polhemus_checkbox = tk.Checkbutton(window, text="Polhemus", variable=POLHEMUS)
polhemus_checkbox.grid(row=1, column=0, sticky="w")
leapmotion_checkbox = tk.Checkbutton(window, text="Leapmotion", variable=LEAPMOTION, command=toggle_leapmotion)
leapmotion_checkbox.grid(row=2, column=0, sticky="w")
vive_checkbox = tk.Checkbutton(window, text="Vive", variable=VIVE)
vive_checkbox.grid(row=3, column=0, sticky="w")

# Leapmotion mode dropdown
# These are the same three modes that can be seen in the Leapmotion Control Panel.
options = ["Desktop", "Head Mounted", "Screentop"]
leapmotion_mode = ttk.Combobox(window, values=options, state="disabled")
leapmotion_mode.set("Leapmotion mode...")
leapmotion_mode.grid(row=2, column=1)

def stop_output():
    '''
    Stops all output of trackers.
    '''
    global STARTED
    if POLHEMUS.get():
        pol.another = False
        pol.stop_event.set()
        if polhemus_thread is not None:
            polhemus_thread.join()  # Wait for the thread to finish
    if LEAPMOTION.get():
        leapm.another = False
        leapm.connection.disconnect()
    if VIVE.get():
        vive.another = False
    STARTED = False

def begin_tracking():
    '''
    Begins output of all selected trackers.
    '''
    # Test if the hz field is an integer
    try:
        hz = int(hz_field.get())
        if hz < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Polling rate error", "Please enter a valid integer for the polling rate.")
        return
    else:
        # Check a valid mode is selected for leapmotion
        if LEAPMOTION.get() and (leapmotion_mode.get() not in ["Desktop", "Head Mounted", "Screentop"]):
            raise ValueError("Please select a valid mode for Leapmotion.")
        global STARTED, start_time
        if not STARTED:
            STARTED = True
            start_time = time.time()
            stopwatch_label.config(text="00:00:00")
            start_stopwatch()
            if POLHEMUS.get():
                pol.stop_event.clear()
                polhemus_thread = threading.Thread(target=pol.output_data, args=(hz,), daemon=True)
                polhemus_thread.start()
            if LEAPMOTION.get():
                leapm.another = True
                leapm.SELECTED_MODE = leapm.tracking_modes[leapmotion_mode.get()]
                leapmotion_thread = threading.Thread(target=leapm.initialise_leapmotion, daemon=True, args=(hz,))
                leapmotion_thread.start()
            if VIVE.get():
                # Initialize OpenVR
                try:
                    vive.openvr.init(vive.openvr.VRApplication_Scene)
                    vive.another = True
                    vive_thread = threading.Thread(target=vive.start_vive, daemon=True, args=(hz,))
                    vive_thread.start()
                # Since VR is the last to be initialised, sending the stop button signal if failed will stop all other threads too
                except:
                    stop_output()
                    stop_button_wrapper()
                    messagebox.showerror("Could not initialize OpenVR", "Please ensure SteamVR is running and a headset is connected.", parent=window)
                    print("Error: Could not initialize OpenVR. Please ensure SteamVR is running and a headset is connected.")

        else:
            print("Already started.")

def open_file_picker():
    if not STARTED:
        file_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP Files", "*.zip")])
        print(file_path)
        file_list = ["polhemus_output.csv", "leapmotion_output.csv"]
        file_list.extend(vive.files)

        if camera.camera_output_file:
            file_list.append(camera.camera_output_file)

        zip_files(file_list, file_path)
    else:
        print("Cannot save file while tracking.")

def start_stopwatch():
    global STARTED
    global counter
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
    with zipfile.ZipFile(zip_name, "w") as zipf:
        for file in files:
            try:
                zipf.write(file, os.path.basename(file))
            except:
                # File does not exist (that tracker or camera must not have been used)
                pass


def select_camera(event):
    global selected_camera_index
    selected_camera_index = int(camera_var.get())
    print(f"Camera {selected_camera_index} selected")

camera_dropdown.bind("<<ComboboxSelected>>", select_camera)

# Help button function
def show_help():
    '''
    This function creates a small pop-up box with helpful information.
    '''
    help_text = (
        "Welcome to the Tracker Interface Help!\n\n"
        "- To start tracking, make sure to select the trackers and set a valid polling rate, no negatives!\n"
        "- The 'Camera' checkbox allows you to select a camera and record video.\n"
        "- If 'Camera' checkbox is selected make sure you select a camera to use\n."
        "- The Select a camera drop down lists numbers that each correspond to a different camera\n."
        "- Use the 'Preview Camera' button to ensure the camera is working.\n"
        "- Click 'Start' to begin tracking and recording.\n"
        "- Click 'Stop' to end the tracking and recording.\n"
        "- Use 'Save zip to...' to save your results in a zip file.\n"
        "\n\n"

        "Quick Troubleshooting\n\n"
        "- If you hit start after selecting a camera and you notice the error getStreamChannelGroup Camera index out of range it can be ignored\n"
        "- If you are noticing data files disappearing when you run the program a second time without saving the files into a zip file it is because it deletes the files in the current directory if they are not moved or saved as a zip\n"
        "- Please view Code documentation if you wish to customise this program."
    )
    messagebox.showinfo("Help", help_text)

# UI Buttons
start_button = tk.Button(window, text="Start", command=start_button_wrapper)
start_button.grid(row=1, column=3, sticky="ew")

stop_button = tk.Button(window, text="Stop", command=stop_button_wrapper, state="disabled")
stop_button.grid(row=2, column=3, sticky="ew")

file_picker_button = tk.Button(window, text="Save zip to...", command=open_file_picker)
file_picker_button.grid(row=3, column=3)

# Add the Help button
help_button = tk.Button(window, text="Help", command=show_help)
help_button.grid(row=4, column=3, sticky="ew", padx=5, pady=5)









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
    try:
        pattern = re.compile(r'.*_data\..*')
        for file in os.listdir('./'):
            if pattern.match(file):
                os.remove(file)
    except:
        pass
    pol.initialise_polhemus(1)
    valid_cameras = camera.find_valid_cameras()
    camera_dropdown["values"] = valid_cameras #populate the camera dropdown
    window.mainloop()
