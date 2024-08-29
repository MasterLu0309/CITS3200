from bvh import Bvh

# Read the BVH file and parse it
with open("BVH-Recording3.bvh") as f:
    bvh_data = Bvh(f.read())

# Extract and print basic information
print(f"Number of frames: {bvh_data.nframes}")
print(f"Frame time: {bvh_data.frame_time}")
print("Joint names:", *bvh_data.get_joints(), sep="\n")

# Function to extract joint rotations
def extract_joint_rotations(bvh_data, joint_name):
    x_rotations = []
    y_rotations = []
    z_rotations = []
    for frame in range(bvh_data.nframes):
        try:
            x_rotations.append(float(bvh_data.frame_joint_channel(frame, joint_name, 'Xrotation')))
            y_rotations.append(float(bvh_data.frame_joint_channel(frame, joint_name, 'Yrotation')))
            z_rotations.append(float(bvh_data.frame_joint_channel(frame, joint_name, 'Zrotation')))
        except ValueError as e:
            print(f"Error: {e}")
            print(f"Available channels for joint '{joint_name}': {bvh_data.joint_channels(joint_name)}")
            break
    return x_rotations, y_rotations, z_rotations
