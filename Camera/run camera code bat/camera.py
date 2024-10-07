import cv2
import datetime
import time

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = None

is_recording = False

prev_frame = None

# Setting the delay time to stop recording
stop_delay = 2
last_motion_time = 0  

if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if prev_frame is None:
        prev_frame = gray
        continue

    frame_delta = cv2.absdiff(prev_frame, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Finding outlines
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Large movements detected
    movement_detected = False
    for contour in contours:
        if cv2.contourArea(contour) < 1000: 
            continue
        movement_detected = True
        last_motion_time = time.time() 
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Starts recording if motion is detected and not in recording
    if movement_detected and not is_recording:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output_{timestamp}.avi"
        print(f"Recording started: {filename}")
        out = cv2.VideoWriter(filename, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
        is_recording = True

    elif not movement_detected and is_recording:
        if time.time() - last_motion_time > stop_delay:
            print("Recording stopped due to no movement...")
            is_recording = False
            out.release()
            out = None

    # Display the real-time timestamp on the frame
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] 
    cv2.putText(frame, current_time, (frame.shape[1] - 400, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Write the frame with the timestamp to the output file if recording
    if is_recording:
        out.write(frame)

    # Show the video feed
    cv2.imshow('Camera Feed', frame)
    cv2.imshow('Frame Delta', frame_delta)

    prev_frame = gray

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("Exiting...")
        break

cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()
