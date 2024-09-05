import tkinter as tk
from tkinter import filedialog, ttk
import threading
import polhemus_interface as pol
import leapmotion_interface as leapm
import shutil
import os
import time


STARTED = False

start_time = None
polhemus_thread = None
leapmotion_thread = None

# Create the main window
window = tk.Tk()
window.title("Tracker Interface")

POLHEMUS = tk.BooleanVar()
LEAPMOTION = tk.BooleanVar()

# Add Label
label = tk.Label(window, text="Polling Rate (Hz):")
label.pack(side=tk.LEFT)

# Add Text Entry Field
hz_field = tk.Entry(window)
hz_field.pack(side=tk.LEFT)

# Add Stopwatch Label
stopwatch_label = tk.Label(window, text="00:00:00.000")
stopwatch_label.pack()

# Add checkboxes
polhemus_checkbox = tk.Checkbutton(window, text="Polhemus", variable=POLHEMUS)
polhemus_checkbox.pack()
leapmotion_checkbox = tk.Checkbutton(window, text="Leapmotion", variable=LEAPMOTION)
leapmotion_checkbox.pack()

# Tkinter comboboxw (dropdown)
options = ["Desktop", "Head Mounted", "Screentop"]
leapmotion_mode = ttk.Combobox(window, values=options, state="readonly")
leapmotion_mode.set("Leapmotion mode")
leapmotion_mode.pack(side=tk.LEFT)

def stop_output():
    global STARTED
    if POLHEMUS.get():
        pol.another = False
    if LEAPMOTION.get():
        leapm.another = False
        leapm.connection.disconnect()
    STARTED = False


def start_output():
    global STARTED
    # Check if hz is valid
    try:
        hz = int(hz_field.get())
    except:
        STARTED = False
        raise ValueError("Please enter a valid integer for the frequency.")

    pol.output_data(hz)

def begin_tracking():
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
    if not STARTED:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        print(file_path)
        shutil.copy("test_output.csv", file_path)
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




# Add Button 1
button1 = tk.Button(window, text="Start", command=begin_tracking)
button1.pack()

# Add Button 2
button2 = tk.Button(window, text="Stop", command=stop_output)
button2.pack()

# File picker
file_picker_button = tk.Button(window, text="Save csv to...", command=open_file_picker)
file_picker_button.pack()

# Start the main event loop
if __name__ == "__main__":
    try:
        os.remove("test_output.csv")
    except:
        pass
    pol.initialise_polhemus(1)
    window.mainloop()