import openvr  # Library to interact with HTC Vive devices (VR system)
import time  # Library for time management (e.g., time tracking, sleep)
import csv  # For reading/writing CSV files
import os  # OS-level operations (e.g., checking file size)
import pandas as pd  # For working with data in DataFrames (used for xlsx output)
import scipy.io as sio  # For saving data in MATLAB's .mat format

# Boolean variable to control indefinite recording loop
another = True

# Set to keep track of created files
files = set()

def get_device_name_type_and_serial(device_index):
    """
    Retrieve the device's name, type (e.g., Headset, Controller, Tracker), and serial number.
    
    :param device_index: The index of the device in the VR system.
    :return: A tuple containing (device_name, device_type, device_serial).
    """
    # Get the device's class/type (e.g., headset, controller)
    device_class = openvr.VRSystem().getTrackedDeviceClass(device_index)

    # Get the device's model number/name
    device_name = openvr.VRSystem().getStringTrackedDeviceProperty(device_index, openvr.Prop_ModelNumber_String)
    
    # Get the device's serial number (unique identifier for the device)
    device_serial = openvr.VRSystem().getStringTrackedDeviceProperty(device_index, openvr.Prop_SerialNumber_String)

    # Determine the type of device based on the class
    if device_class == openvr.TrackedDeviceClass_HMD:
        device_type = "Headset"
    elif device_class == openvr.TrackedDeviceClass_Controller:
        device_type = "Controller"
    elif device_class == openvr.TrackedDeviceClass_TrackingReference:
        device_type = "Tracker"
    else:
        device_type = "Unknown"  # If not identified, it falls under "Unknown"

    return device_name, device_type, device_serial

def get_tracker_data():
    """
    Retrieves tracking data (pose) for all connected devices and categorizes them by type.
    
    :return: A dictionary containing device data categorized by type and the data completion rate.
    """
    # Array to hold pose data for up to the maximum number of devices
    poses = (openvr.TrackedDevicePose_t * openvr.k_unMaxTrackedDeviceCount)()
    
    # Get the absolute pose (position and orientation) of each tracked device
    openvr.VRSystem().getDeviceToAbsoluteTrackingPose(openvr.TrackingUniverseStanding, 0, poses)

    # Dictionary to categorize devices by type (e.g., Headset, Controller, etc.)
    device_data = {"Headset": [], "Controller": [], "Tracker": [], "Unknown": []}
    
    # Track the total number of devices and those with valid pose data
    total_devices = 0
    successful_reads = 0

    # Loop through all devices and collect their pose data
    for i in range(len(poses)):
        if not openvr.VRSystem().isTrackedDeviceConnected(i):
            continue  # Skip if the device is not connected

        total_devices += 1
        if poses[i].bPoseIsValid:  # Check if the pose is valid (i.e., usable tracking data)
            successful_reads += 1
            device_name, device_type, device_serial = get_device_name_type_and_serial(i)
            
            # Get the device's transformation matrix (pose) for its position/orientation
            tracker_pose = poses[i].mDeviceToAbsoluteTracking
            # Flatten the 3x4 matrix into a single list
            flat_pose = [item for row in tracker_pose for item in row]
            
            # Store the device's data in the corresponding category
            device_data[device_type].append([i, device_name, device_serial] + flat_pose)
        else:
            # Notify if a device has invalid pose data
            print(f"Warning: Device {i} has invalid pose.")

    # Calculate the percentage of devices with valid data
    completion_rate = (successful_reads / total_devices) * 100
    print(f"Data completion rate: {completion_rate:.2f}%")
    
    return device_data, completion_rate

def write_data_to_files(device_data, export_format="csv"):
    """
    Writes the tracking data to files (CSV, XLSX, TXT, or MAT format) for each device.
    
    :param device_data: Dictionary containing tracking data for each device type.
    :param export_format: The format in which to save the data ("csv", "xlsx", "txt", or "mat").
    """
    # Loop through each type of device (Headset, Controller, Tracker, Unknown)
    for device_type, devices in device_data.items():
        # Loop through each device's data
        for device in devices:
            device_id, device_name, device_serial, *pose_data = device
            # Create the file name based on device type and serial number
            file_name = f"{device_type.lower()}_{device_serial}_data.{export_format}"
            # Keep track of the file being created
            files.add(file_name)

            try:
                # Write data in the chosen format
                if export_format == "csv":
                    # Write to a CSV file (append mode)
                    with open(file_name, mode="a", newline="") as csv_file:
                        csv_writer = csv.writer(csv_file)
                        # If file is empty, write the header
                        if os.path.getsize(file_name) == 0:
                            header = ["Timestamp", "Device ID", "Device Name", "Device Serial", "M00", "M01", "M02", "M03", 
                                      "M10", "M11", "M12", "M13", "M20", "M21", "M22", "M23"]
                            csv_writer.writerow(header)
                        # Write the device data along with a timestamp
                        csv_writer.writerow([time.time()] + [device_id, device_name, device_serial] + pose_data)
                elif export_format == "xlsx":
                    # Write data to an Excel file
                    df = pd.DataFrame([device], columns=["Device ID", "Device Name", "Device Serial", 
                                                         "M00", "M01", "M02", "M03", "M10", "M11", "M12", "M13",
                                                         "M20", "M21", "M22", "M23"])
                    df.to_excel(file_name, index=False)
                elif export_format == "txt":
                    # Write data to a text file
                    with open(file_name, mode="a") as txt_file:
                        txt_file.write(str(device) + "\n")
                elif export_format == "mat":
                    # Write data to a .mat file (MATLAB format)
                    sio.savemat(file_name, {f"{device_type.lower()}_{device_serial}": device})
                else:
                    raise ValueError(f"Unsupported export format: {export_format}")
            except Exception as e:
                # Print any errors that occur during file writing
                print(f"Error writing to file {file_name}: {e}")

def record_for_preset_time(duration_seconds, hz, export_format="csv"):
    """
    Records device tracking data for a preset time duration at a given frequency.
    
    :param duration_seconds: The total duration (in seconds) to record.
    :param hz: The frequency of data collection (in Hz, i.e., number of recordings per second).
    :param export_format: The format in which to save the data (default is "csv").
    """
    start_time = time.time()  # Start timer
    while time.time() - start_time < duration_seconds:  # Loop until the preset duration is reached
        device_data, completion_rate = get_tracker_data()  # Get tracking data
        write_data_to_files(device_data, export_format)  # Save the data
        time.sleep(1/hz)  # Wait for the next data collection (based on the frequency)
    print("Recording completed.")

def record_indefinitely(hz, export_format="csv"):
    """
    Records device tracking data indefinitely (until manually interrupted).
    
    :param hz: The frequency of data collection (in Hz, i.e., number of recordings per second).
    :param export_format: The format in which to save the data (default is "csv").
    """
    while another:  # Continue recording until 'another' is set to False
        device_data, completion_rate = get_tracker_data()  # Get tracking data
        write_data_to_files(device_data, export_format)  # Save the data
        time.sleep(1/hz)  # Wait for the next data collection (based on the frequency)

def map_device_id_to_physical_tracker():
    """
    Maps each device ID to a physical tracker (Headset, Controller, Tracker) and prints the mapping.
    
    :return: A dictionary mapping device IDs to their type, name, and serial number.
    """
    device_mapping = {}
    for i in range(openvr.k_unMaxTrackedDeviceCount):
        if openvr.VRSystem().isTrackedDeviceConnected(i):  # Check if the device is connected
            device_name, device_type, device_serial = get_device_name_type_and_serial(i)
            device_mapping[i] = (device_type, device_name, device_serial)
    
    # Print the device mapping (ID -> Type, Name, Serial Number)
    print("Device Mapping:")
    for device_id, (device_type, device_name, device_serial) in device_mapping.items():
        print(f"ID {device_id}: {device_type}, Name: {device_name}, Serial: {device_serial}")
    
    return
