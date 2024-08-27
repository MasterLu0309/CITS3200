from bvh import Bvh

# Read the BVH file and parse it
with open("BVH-Recording3.bvh") as f:
    bvh_data = Bvh(f.read())

# Extract and print basic information
print(f"Number of frames: {bvh_data.nframes}")
print(f"Frame time: {bvh_data.frame_time}")
print("Joint names:", *bvh_data.get_joints(), sep="\n")
