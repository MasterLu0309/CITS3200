import cv2
import datetime
import time

cap = None
out = None
is_recording = False

def initialize_camera(camera_index):
    """Initialize the camera and check if it's opened successfully."""
    global cap
    cap = cv2.VideoCapture(camera_index)  # Open the selected camera

    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_index}")
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
        print("Failsafe reached")
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
    global out, is_recording

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

        # Bring the window to the foreground
        cv2.setWindowProperty('Camera Feed', cv2.WND_PROP_TOPMOST, 1)

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

def find_valid_cameras():
    """Scan and return a list of valid camera indices."""
    max_failed_attempts = 2  # Stop after 2 consecutive failed camera attempts
    failed_attempts = 0
    available_cameras = list(range(10))  # Check up to 10 camera indices
    valid_cameras = []

    for i in available_cameras:
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            valid_cameras.append(i)
            failed_attempts = 0  # Reset failed attempts after a success
            cap.release()
        else:
            failed_attempts += 1
            cap.release()
            if failed_attempts >= max_failed_attempts:
                print("Stopping search after encountering consecutive failed attempts.")
                break

    if not valid_cameras:
        print("No cameras detected.")
    return valid_cameras

def preview_camera(camera_index):
    """Preview the selected camera for 3 seconds and then close it."""
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_index} for preview.")
        return

    start_time = time.time()
    while time.time() - start_time < 3:  # Preview for 3 seconds
        ret, frame = cap.read()
        if not ret:
            print(f"Error: Could not read frame from camera {camera_index}.")
            break
        
        cv2.imshow(f'Preview of Camera {camera_index}', frame)

        # Bring the preview window to the foreground
        cv2.setWindowProperty(f'Preview of Camera {camera_index}', cv2.WND_PROP_TOPMOST, 1)

        # Update the window and ensure proper rendering
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and properly close the window
    cap.release()
    cv2.destroyWindow(f'Preview of Camera {camera_index}')
    
    # Add a small wait to ensure OpenCV processes the window closure
    cv2.waitKey(1)

def start_camera():
    """Start the camera and begin processing frames with the system's default settings."""
    valid_cameras = find_valid_cameras()

    if not valid_cameras:
        print("No cameras available to select.")
        return

    # Ask the user to preview and select a camera
    while True:
        print(f"Valid camera indices: {valid_cameras}")
        try:
            camera_index = int(input(f"Enter a camera index to preview from the valid cameras {valid_cameras}: "))
            if camera_index not in valid_cameras:
                print(f"Invalid index. Please select from the valid cameras {valid_cameras}.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        # Preview the selected camera for 3 seconds
        preview_camera(camera_index)

        # Ask if the user wants to use the previewed camera
        choice = input(f"Do you want to use Camera {camera_index}? (y/n): ").lower()
        if choice == 'y':
            break

    if not initialize_camera(camera_index):
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
