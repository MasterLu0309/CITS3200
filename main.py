import tkinter as tk
import threading
import polhemus_interface as pol

# Create the main window
window = tk.Tk()

# Add Text Entry Field
hz_field = tk.Entry(window)
hz_field.pack()

# Add widgets and functionality here
def stop_output():
    pol.another = False

def start_output():
    # Check if hz is valid
    try:
        hz = int(hz_field.get())
    except:
        raise ValueError("Please enter a valid integer for the frequency.")

    pol.output_data(hz)

def begin_tracking():
    threading.Thread(target=start_output).start()

# Add Button 1
button1 = tk.Button(window, text="Start", command=begin_tracking)
button1.pack()

# Add Button 2
button2 = tk.Button(window, text="Stop", command=stop_output)
button2.pack()

# Start the main event loop
if __name__ == "__main__":
    pol.initialise_polhemus(1)
    window.mainloop()