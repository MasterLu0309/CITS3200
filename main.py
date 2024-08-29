import tkinter as tk
from tkinter import filedialog
import threading
import polhemus_interface as pol
from leapmotion_interface import MyListener
import shutil
import os
import time
import leap

STARTED = False

start_time = None

# Create the main window
window = tk.Tk()
window.title("Tracker Interface")

# Add Label
label = tk.Label(window, text="Polling Rate (Hz):")
label.pack(side=tk.LEFT)

# Add Text Entry Field
hz_field = tk.Entry(window)
hz_field.pack(side=tk.LEFT)

# Add Stopwatch Label
stopwatch_label = tk.Label(window, text="00:00:00.000")
stopwatch_label.pack()

# Add widgets and functionality here
def stop_output():
    global STARTED
    pol.another = False
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
        threading.Thread(target=start_output, daemon=True).start()
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

def initialise_leapmotion():
    my_listener = MyListener()

    connection = leap.Connection()
    connection.add_listener(my_listener)

    running = True

    with connection.open():
        connection.set_tracking_mode(leap.TrackingMode.Desktop)
        while running:
            time.sleep(1)


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
    threading.Thread(target=initialise_leapmotion, daemon=True).start()
    window.mainloop()