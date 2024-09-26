import steamvr

# Initialize SteamVR
try:
    steamvr.init()
except Exception as e:
    print(f"Failed to initialize SteamVR: {e}")
    exit(1)  # Exit the program if initialization fails
# Get the number of tracked devices
num_devices = steamvr.get_device_count()

# Check if devices are trackers and gather pose data
device_data = []

# Iterate through devices and check if they are trackers
for i in range(num_devices):
    try:
        device_class = steamvr.get_device_class(i)        
        if device_class == steamvr.DeviceClass.GenericTracker:
            # Get the device's pose (position and orientation)
            pose = steamvr.get_device_pose(i)           
            if pose is not None:
                position = pose.m[12:15]  # Extract position (x, y, z)
                 # Extract orientation rows from matrix
                orientation = [
                    pose.m[0:3],  # First row
                    pose.m[4:7],  # Second row
                    pose.m[8:11]  # Third row
                ]
                print(f"Tracker {i} position: {position}, orientation: {orientation}")
                device_data.append({
                    'device_id': i,
                    'position': position,
                    'orientation': orientation
                })
            else:
                print(f"Tracker {i} pose data is not available.")
        else:
            print(f"Device {i} is not a tracker, it's a {device_type}.")
    except Exception as e:
        print(f"Error accessing device {i}: {e}")
return device_data
