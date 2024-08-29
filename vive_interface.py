import triad_openvr

v = triad_openvr.triad_openvr()
v.print_discovered_objects()

if len(v.devices["tracker"]) == 0:
    print("No trackers found!")
    exit(1)

while True:
    for device_key in v.devices["tracker"]:
        tracker = v.devices["tracker"][device_key]
        print(f"Tracker {device_key}:")
        print(f"  Position: {tracker.get_pose_matrix()[:3, 3]}")
