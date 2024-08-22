import tkinter as tk
from tkinter import filedialog
import threading
import polhemus_interface as pol
import shutil
import os

STARTED = False

# Create the main window
window = tk.Tk()
window.title("Tracker Interface")

# Add Label
label = tk.Label(window, text="Polling Rate (Hz):")
label.pack(side=tk.LEFT)

# Add Text Entry Field
hz_field = tk.Entry(window)
hz_field.pack(side=tk.LEFT)

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
    global STARTED
    if not STARTED:
        STARTED = True
        threading.Thread(target=start_output).start()
    else:
        print("Already started.")

def open_file_picker():
    if not STARTED:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        print(file_path)
        shutil.copy("test_output.csv", file_path)
    else:
        print("Cannot save file while tracking.")


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
    os.remove("test_output.csv")
    pol.initialise_polhemus(1)
    window.mainloop()