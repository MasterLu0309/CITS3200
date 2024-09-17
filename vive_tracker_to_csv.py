import openvr
import time
import csv

openvr.init(openvr.VRApplication_Scene)

def get_tracker_data():
    poses = (openvr.TrackedDevicePose_t * openvr.k_unMaxTrackedDeviceCount)()  
    openvr.VRSystem().getDeviceToAbsoluteTrackingPose(openvr.TrackingUniverseStanding, 0, poses)
    
    tracker_data = []
    for i in range(len(poses)):  
        if poses[i].bPoseIsValid:
            device_class = openvr.VRSystem().getTrackedDeviceClass(i)
            if device_class == openvr.TrackedDeviceClass_TrackingReference:
                tracker_pose = poses[i].mDeviceToAbsoluteTracking
                flat_pose = [item for row in tracker_pose for item in row]
                serial_number = openvr.VRSystem().getStringTrackedDeviceProperty(i, openvr.Prop_SerialNumber_String)
                tracker_data.append([i] + flat_pose)  
    return tracker_data

csv_file = open("tracker_data.csv", mode="w", newline="")
csv_writer = csv.writer(csv_file)
header = ["Tracker ID", "M00", "M01", "M02", "M03", "M10", "M11", "M12", "M13", "M20", "M21", "M22", "M23"]
csv_writer.writerow(header)

try:
    while True:
        tracker_data = get_tracker_data()
        for data in tracker_data:
            csv_writer.writerow(data) 
        time.sleep(0.1) 
except KeyboardInterrupt:
    print("Exiting...")
finally:
    csv_file.close()
    openvr.shutdown()
