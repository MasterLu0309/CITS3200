from bvh import Bvh
import numpy as np

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

# Extract rotations for RIGHT_UPPER_LEG and RIGHT_LOWER_LEG
upper_x_rot, upper_y_rot, upper_z_rot = extract_joint_rotations(bvh_data, 'RIGHT_UPPER_LEG')
lower_x_rot, lower_y_rot, lower_z_rot = extract_joint_rotations(bvh_data, 'RIGHT_LOWER_LEG')

# Calculate the angle between RIGHT_UPPER_LEG and RIGHT_LOWER_LEG
angles = []
for i in range(len(upper_x_rot)):
    upper_vector = np.array([upper_x_rot[i], upper_y_rot[i], upper_z_rot[i]])
    lower_vector = np.array([lower_x_rot[i], lower_y_rot[i], lower_z_rot[i]])
    dot_product = np.dot(upper_vector, lower_vector)
    norm_upper = np.linalg.norm(upper_vector)
    norm_lower = np.linalg.norm(lower_vector)
    cos_angle = dot_product / (norm_upper * norm_lower)
    angle = np.arccos(cos_angle)
    angles.append(np.degrees(angle))
