import openvr
import time

openvr.init(openvr.VRApplication_Scene)

def get_tracker_data():
    poses = (openvr.TrackedDevicePose_t * openvr.k_unMaxTrackedDeviceCount) () # intialise poses array
    
    openvr.VRSystem().getDeviceToAbsoluteTrackingPose(openvr.TrackingUniverseStanding, 0, poses)

    poses_length = len(poses)
    print(f"poses array length: {poses_length}")
    for i in range(poses_length): #loop through all detected trackers
        #print(f"poses array length: {poses_length}")
        if poses[i].bPoseIsValid:
            device_class = openvr.VRSystem().getTrackedDeviceClass(i)
            if device_class == openvr.TrackedDeviceClass_TrackingReference:
                print(f"Tracker {i} data:")
                print(poses[i].mDeviceToAbsoluteTracking)

try:
    while True:
        get_tracker_data()
        time.sleep(0.1)  # Polling interval
except KeyboardInterrupt:
    print("Exiting...")
finally:
    openvr.shutdown()
