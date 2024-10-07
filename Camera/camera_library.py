# camera_interface.py

import cv2  # Import OpenCV library for computer vision tasks
import datetime  # Import datetime module to work with timestamps
import time  # Import time module to manage timing

# Global variables for camera functionality
cap = None  
out = None  
is_recording = False 

def initialize_camera():
    """Initialize the camera and check if it's opened successfully."""
    global cap
    cap = cv2.VideoCapture(0) 

    if not cap.isOpened():
        print("Error: Could not open camera")  
        return False  
    return True 

def start_recording(filename):
    """Start recording to a video file."""
    global out, is_recording
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
    out = cv2.VideoWriter(filename, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))  
    is_recording = True  
    print(f"Recording started: {filename}") 

def stop_recording():
    """Stop recording and release the video writer."""
    global out, is_recording
    if is_recording:
        out.release() 
        print("Recording stopped")  
    is_recording = False 

def process_frame(polling_rate):
    """Process video frames from the camera."""
    global out, is_recording
    last_poll_time = time.time()

    while True:
        current_time = time.time()  

        # Check if enough time has passed since the last frame was captured
        if current_time - last_poll_time >= polling_rate:
            ret, frame = cap.read()  
            if not ret:
                print("Error: Could not read frame")  
                break  

            # Display the real-time timestamp on the video frame
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            cv2.putText(frame, timestamp, (frame.shape[1] - 400, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            # Display the video feed in a window
            cv2.imshow('Camera Feed', frame)

            # Check for user input to start or stop recording
            key = cv2.waitKey(1) & 0xFF 

            # Start recording if 'r' is pressed
            if key == ord('r') and not is_recording:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"output_{timestamp}.mov"  
                start_recording(filename) 
            
            # Stop recording if 's' is pressed
            elif key == ord('s') and is_recording:
                stop_recording()  

            # Write the current frame to the output file if recording
            if is_recording:
                out.write(frame)

            # Update the last poll time to the current time
            last_poll_time = current_time  

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exit") 
            break  

def start_camera(polling_rate):
    """Start the camera and begin processing frames."""
    if not initialize_camera():  
        return  
    process_frame(polling_rate)  

def cleanup():
    """Clean up resources after exiting."""
    if cap is not None:
        cap.release()  
    if out is not None:
        out.release()  
    cv2.destroyAllWindows()  