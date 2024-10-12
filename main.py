import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
import polhemus_interface as pol
import leapmotion_interface as leapm
import vive_data_tracker as vive
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

# Create the main window
window = tk.Tk()
window.title("Tracker Interface")
window.resizable(False, False)

# Variables correspond to the UI checkboxes for respective trackers.
POLHEMUS = tk.BooleanVar()
LEAPMOTION = tk.BooleanVar()
VIVE = tk.BooleanVar()

# POLLING RATE
label = tk.Label(window, text="Polling Rate (Hz):")
label.grid(row=0, column=0)
hz_field = tk.Entry(window)
hz_field.grid(row=0, column=1)

# STOPWATCH
stopwatch_label = tk.Label(window, text="00:00:00.000")
stopwatch_label.grid(row=0, column=3)

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
    begin_tracking()
    toggle_stop()

def stop_button_wrapper():
    stop_output()
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


def start_output():
    '''
    Begins output of Polhemus data.
    '''
    global STARTED
    # Check if hz is valid
    try:
        hz = int(hz_field.get())
    except:
        STARTED = False
        raise ValueError("Please enter a valid integer for the frequency.")

    pol.output_data(hz)

def hz_messagebox():
    messagebox.showerror("Polling rate error", "Please enter a valid integer for the polling rate.", parent=window)

def begin_tracking():
    '''
    Begins output of all selected trackers.
    '''
    # Test if the hz field is an integer
    try:
        _ = int(hz_field.get())
    except:
        hz_messagebox()
        return
    if int(hz_field.get()) <= 0:
        hz_messagebox()
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
                polhemus_thread = threading.Thread(target=start_output, daemon=True)
                polhemus_thread.start()
            if LEAPMOTION.get():
                leapm.another = True
                leapm.SELECTED_MODE = leapm.tracking_modes[leapmotion_mode.get()]
                leapmotion_thread = threading.Thread(target=leapm.initialise_leapmotion, daemon=True, args=(int(hz_field.get()),))
                leapmotion_thread.start()
            if VIVE.get():
                # Initialize OpenVR
                try:
                    vive.openvr.init(vive.openvr.VRApplication_Scene)
                    vive.another = True
                    vive_thread = threading.Thread(target=vive.start_vive, daemon=True, args=(int(hz_field.get()),))
                    vive_thread.start()
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
                # File does not exist (that tracker must not have been used)
                pass


# UI Buttons
start_button = tk.Button(window, text="Start", command=start_button_wrapper)
start_button.grid(row=1, column=3, sticky="ew")

stop_button = tk.Button(window, text="Stop", command=stop_button_wrapper, state="disabled")
stop_button.grid(row=2, column=3, sticky="ew")

file_picker_button = tk.Button(window, text="Save zip to...", command=open_file_picker)
file_picker_button.grid(row=3, column=3)

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
    window.mainloop()