import steamvr

# Initialize SteamVR
steamvr.init()

# Get the number of tracked devices
num_devices = steamvr.get_device_count()

# Iterate through devices and check if they are trackers
for i in range(num_devices):
  device_class = steamvr.get_device_class(i)
    if device_class == steanvr.DeviceClass.GenericTracker:
      print("Tracker on", i, "found")
