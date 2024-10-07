import openvr
import time
import csv
import os
import pandas as pd  
import scipy.io as sio  

another = True
files = []

# Initialize OpenVR
try:
    openvr.init(openvr.VRApplication_Scene)
except:
    print("Error: Could not initialize OpenVR. Please ensure SteamVR is running and a headset is connected.")

def get_device_name_type_and_serial(device_index):
    """Retrieve the name, type, and serial number of the device."""
    device_class = openvr.VRSystem().getTrackedDeviceClass(device_index)

    # Get the device model or name
    device_name = openvr.VRSystem().getStringTrackedDeviceProperty(device_index, openvr.Prop_ModelNumber_String)
    
    # Get the device serial number
    device_serial = openvr.VRSystem().getStringTrackedDeviceProperty(device_index, openvr.Prop_SerialNumber_String)

    # Determine device type
    if device_class == openvr.TrackedDeviceClass_HMD:
        device_type = "Headset"
    elif device_class == openvr.TrackedDeviceClass_Controller:
        device_type = "Controller"
    elif device_class == openvr.TrackedDeviceClass_TrackingReference:
        device_type = "Tracker"
    else:
        device_type = "Unknown"

    return device_name, device_type, device_serial

def get_tracker_data():
    """Get tracking data for all devices and categorize by type."""
    poses = (openvr.TrackedDevicePose_t * openvr.k_unMaxTrackedDeviceCount)()
    openvr.VRSystem().getDeviceToAbsoluteTrackingPose(openvr.TrackingUniverseStanding, 0, poses)

    device_data = {"Headset": [], "Controller": [], "Tracker": [], "Unknown": []}
    total_devices = 0
    successful_reads = 0

    for i in range(len(poses)):
        total_devices += 1
        if poses[i].bPoseIsValid:
            successful_reads += 1
            device_name, device_type, device_serial = get_device_name_type_and_serial(i)
            tracker_pose = poses[i].mDeviceToAbsoluteTracking
            flat_pose = [item for row in tracker_pose for item in row]
            device_data[device_type].append([i, device_name, device_serial] + flat_pose)
        else:
            print(f"Warning: Device {i} has invalid pose.")

    completion_rate = (successful_reads / total_devices) * 100
    print(f"Data completion rate: {completion_rate:.2f}%")
    
    return device_data, completion_rate

def write_data_to_files(device_data, export_format="csv"):
    """Append data to separate files based on device type and export format."""
    for device_type, data in device_data.items():
        file_name = f"{device_type.lower()}_data.{export_format}"
        files.append(file_name)

        try:
            if export_format == "csv":
                with open(file_name, mode="a", newline="") as csv_file:
                    csv_writer = csv.writer(csv_file)
                    if os.path.getsize(file_name) == 0:
                        header = ["Device ID", "Device Name", "Device Serial", "M00", "M01", "M02", "M03", 
                                  "M10", "M11", "M12", "M13", "M20", "M21", "M22", "M23"]
                        csv_writer.writerow(header)
                    csv_writer.writerows(data)
            elif export_format == "xlsx":
                df = pd.DataFrame(data, columns=["Device ID", "Device Name", "Device Serial", 
                                                  "M00", "M01", "M02", "M03", "M10", "M11", "M12", "M13",
                                                  "M20", "M21", "M22", "M23"])
                df.to_excel(file_name, index=False)
            elif export_format == "txt":
                with open(file_name, mode="a") as txt_file:
                    txt_file.write("\n".join(str(row) for row in data) + "\n")
            elif export_format == "mat":
                sio.savemat(file_name, {device_type.lower(): data})
            else:
                raise ValueError(f"Unsupported export format: {export_format}")
        except Exception as e:
            print(f"Error writing to file {file_name}: {e}")

def record_for_preset_time(duration_seconds, hz, export_format="csv"):
    """Record tracker data for a preset duration."""
    start_time = time.time()
    while time.time() - start_time < duration_seconds:
        device_data, completion_rate = get_tracker_data()
        write_data_to_files(device_data, export_format)
        time.sleep(1/hz)
    print("Recording completed.")

def record_indefinitely(hz, export_format="csv"):
    """Record tracker data indefinitely until interrupted."""
    while another:
        device_data, completion_rate = get_tracker_data()
        write_data_to_files(device_data, export_format)
        time.sleep(1/hz)

def map_device_id_to_physical_tracker():
    """Map each device ID to a physical tracker for easier visualization."""
    device_mapping = {}
    for i in range(openvr.k_unMaxTrackedDeviceCount):
        if openvr.VRSystem().isTrackedDeviceConnected(i):
            device_name, device_type, device_serial = get_device_name_type_and_serial(i)
            device_mapping[i] = (device_type, device_name, device_serial)
    print("Device Mapping:")
    for device_id, (device_type, device_name, device_serial) in device_mapping.items():
        print(f"ID {device_id}: {device_type}, Name: {device_name}, Serial: {device_serial}")
    return device_mapping


def start_vive(hz: int):
    map_device_id_to_physical_tracker()
    record_indefinitely(hz)

if __name__ == "__main__":
    try:
        preset_time = 60  # Record for 60 seconds (can be adjusted)
        export_format = "csv"  # Change format to "xlsx", "txt", or "mat" if desired
        map_device_id_to_physical_tracker()
        record_for_preset_time(preset_time, export_format)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        openvr.shutdown()
