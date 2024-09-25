import steamvr

# Initialize SteamVR
try:
    steamvr.init()
except Exception as e:
    print(f"Failed to initialize SteamVR: {e}")
    exit(1)  # Exit the program if initialization fails
# Get the number of tracked devices
num_devices = steamvr.get_device_count()

# Iterate through devices and check if they are trackers
for i in range(num_devices):
  device_class = steamvr.get_device_class(i)
    if device_class == steanvr.DeviceClass.GenericTracker:
      # Get the device's pose (position and orientation)
      pose = steamvr.get_device_pose(i)
      position = pose.m[12:15] # Extract position (x, y, z)
      print(f"Tracker {i} position {position}")
