from bvh import Bvh

# Read the BVH file and parse it
with open("BVH-Recording3.bvh") as f:
    bvh_data = Bvh(f.read())
