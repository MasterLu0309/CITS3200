import openvr
import time
import csv
import os  # Ensure this import is present

# Initialize OpenVR
openvr.init(openvr.VRApplication_Scene)

def get_device_name_and_type(device_index):
    """Retrieve the name and type of the device."""
    # Get the device class
    device_class = openvr.VRSystem().getTrackedDeviceClass(device_index)

    # Get the device model or name
    device_name = openvr.VRSystem().getStringTrackedDeviceProperty(device_index, openvr.Prop_ModelNumber_String)

    # Determine device type
    if device_class == openvr.TrackedDeviceClass_HMD:
        device_type = "Headset"
    elif device_class == openvr.TrackedDeviceClass_Controller:
        device_type = "Controller"
    elif device_class == openvr.TrackedDeviceClass_TrackingReference:
        device_type = "Tracker"
    else:
        device_type = "Unknown"

    return device_name, device_type

def get_tracker_data():
    """Get tracking data for all devices and categorize by type."""
    poses = (openvr.TrackedDevicePose_t * openvr.k_unMaxTrackedDeviceCount)()
    openvr.VRSystem().getDeviceToAbsoluteTrackingPose(openvr.TrackingUniverseStanding, 0, poses)

    device_data = {"Headset": [], "Controller": [], "Tracker": [], "Unknown": []}

    for i in range(len(poses)):
        if poses[i].bPoseIsValid:
            # Get the name and type of the device
            device_name, device_type = get_device_name_and_type(i)

            # Get the pose data
            tracker_pose = poses[i].mDeviceToAbsoluteTracking
            flat_pose = [item for row in tracker_pose for item in row]
            device_data[device_type].append([i, device_name] + flat_pose)

    return device_data

def write_data_to_files(device_data):
    """Append data to separate CSV files based on device type."""
    for device_type, data in device_data.items():
        file_name = f"{device_type.lower()}_data.csv"

        try:
            # Open CSV file for appending
            with open(file_name, mode="a", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                # Write CSV header if the file is new
                if os.path.getsize(file_name) == 0:
                    header = ["Device ID", "Device Name", "M00", "M01", "M02", "M03", "M10", "M11", "M12", "M13", "M20", "M21", "M22", "M23"]
                    csv_writer.writerow(header)
                # Write data rows, one reading per line
                csv_writer.writerows(data)
        except PermissionError as e:
            print(f"PermissionError: Unable to write to file {file_name}. {e}")
        except Exception as e:
            print(f"Error writing to file {file_name}: {e}")

# Main loop
try:
    while True:
        device_data = get_tracker_data()
        write_data_to_files(device_data)
        time.sleep(1)  # Increased delay to allow for more data collection
except KeyboardInterrupt:
    print("Exiting...")
finally:
    openvr.shutdown()
