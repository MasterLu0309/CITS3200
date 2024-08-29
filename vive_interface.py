import steamvr

# Initialize SteamVR
steamvr.init()

# Get the number of tracked devices
num_devices = steamvr.get_device_count()
