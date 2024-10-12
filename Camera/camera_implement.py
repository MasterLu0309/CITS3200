import cv2
import datetime

cap = None
out = None
is_recording = False

def initialize_camera():
    """Initialize the camera and check if it's opened successfully."""
    global cap
    cap = cv2.VideoCapture(0)  # Open the default camera (0)

    if not cap.isOpened():
        print("Error: Could not open camera")
        return False  
    return True  

def start_recording():
    """Start recording to a video file using the camera's default FPS and resolution."""
    global out, is_recording
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output_{timestamp}.mov"  
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Get the system's default FPS and resolution
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:  # If camera doesn't return FPS, use a fallback
        print("failsafe reached")
        fps = 30.0

    # Get the default resolution
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create VideoWriter object with the default FPS and resolution
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    is_recording = True  
    print(f"Recording started at {fps} FPS with resolution {width}x{height}: {filename}")

def stop_recording():
    """Stop recording and release the video writer."""
    global out, is_recording
    if is_recording:
        out.release()  
        print("Recording stopped")  
    is_recording = False  

def process_frame():
    """Process video frames from the camera."""
    global out, is_recording, exit_flag

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break  

        # Display the real-time timestamp on the video frame
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # Display the video feed in a window
        cv2.imshow('Camera Feed', frame)

        # Write to file if recording
        if is_recording:
            out.write(frame)

        # Check for key press events to start/stop recording or exit
        key = cv2.waitKey(1) & 0xFF
        if key == ord('r') and not is_recording:
            start_recording()
        elif key == ord('s') and is_recording:
            stop_recording()
        elif key == ord('q'):
            print("Exit")
            break  

    stop_recording()

def start_camera():
    """Start the camera and begin processing frames with the system's default settings."""
    if not initialize_camera():
        return
    process_frame()

def stop_camera():
    """Clean up resources after stopping the camera."""
    global cap
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    try:
        start_camera()
    finally:
        stop_camera()
