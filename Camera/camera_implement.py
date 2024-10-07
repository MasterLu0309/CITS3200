# Uncomment the following lines to install the required packages if you haven't already.
# pip install opencv-python
# pip install opencv-contrib-python

import cv2  # Import OpenCV library for computer vision tasks
import datetime  # Import datetime module to work with timestamps
import time  # Import time module to manage timing

# Start capturing video from the default camera (0)
cap = cv2.VideoCapture(0)

# Define the codec for the video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = None  # Initialize video writer variable

# Flag to indicate if recording is in progress
is_recording = False

# Set polling rate for 10 FPS (0.1 seconds per frame)
polling_rate = 0.1  
last_poll_time = time.time()  

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera")  # Print error message if camera fails to open
    exit()  # Exit the program

# Main loop for processing video frames
while True:
    current_time = time.time()  # Get the current time

    # Check if enough time has passed since the last frame was captured
    if current_time - last_poll_time >= polling_rate:
        ret, frame = cap.read()  
        if not ret:
            print("Error: Could not read frame")  # Print error if the frame is not read
            break  # Exit the loop

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
            print(f"Recording started: {filename}")  
            out = cv2.VideoWriter(filename, fourcc, 20.0, (frame.shape[1], frame.shape[0])) 
            is_recording = True  
        
        # Stop recording if 's' is pressed
        elif key == ord('s') and is_recording:
            print("Recording stopped")  
            is_recording = False 
            out.release() 
            out = None  
        
        # Write the current frame to the output file if recording
        if is_recording:
            out.write(frame)

      

        # Update the last poll time to the current time
        last_poll_time = current_time  

        #checking how long code process took
        elapsed_time = time.time() - current_time
        print(f"Elapsed time for frame processing: {elapsed_time:.4f} seconds")  # Print elapsed time

    # Press 'q' to exit the loop
    key = cv2.waitKey(1) & 0xFF  
    if key == ord('q'):
        print("Exit") 
        break  

# Clean up resources after exiting the loop
cap.release()  # Release the camera resource
if out is not None:
    out.release()  # Release the video writer if it exists
cv2.destroyAllWindows()  # Close all OpenCV windows
