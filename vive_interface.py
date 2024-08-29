import triad_openvr

v = triad_openvr.triad_openvr()
v.print_discovered_objects()

if len(v.devices["tracker"]) == 0:
    print("No trackers found!")
    exit(1)
