import leap
import time

# Requires Gemini Ultraleap Hand Tracking software
# https://developer.leapmotion.com/tracking-software-download

# Once installed the Ultraleap Tracking Service must be running

# How to compile leapmotion api for use in any python version
# 1. Install above
# 2. Activate project venv
# 3. Clone `leapc-python-bindings` repo to a directory in project
# 4. `pip install -r requirements.txt` from cloned repo
# 5. `python -m build .\leapc\leapc-cffi` from cloned repo
# 6. `pip install .\leapc\leapc-cffi\dist\leapc_cffi-0.0.1.tar.gz` from cloned repo
# 7. `pip install .\leapc\leapc-python-api` from cloned repo

class MyListener(leap.Listener):
    def __init__(self):
        self.hands = []
    
    def on_connection_event(self, event):
        print("Connected")

    def on_device_event(self, event):
        try:
            with event.device.open():
                info = event.device.get_info()
        except leap.LeapCannotOpenDeviceError:
            info = event.device.get_info()

        print(f"Found device {info.serial}")

    def on_tracking_event(self, event):
        self.hands = event.hands


def initialise_leapmotion(hz: int):
    hand_data = {}
    digits = ["thumb", "index", "middle", "ring", "pinky"]
    bones = ["metacarpal", "proximal", "intermediate", "distal"]
    my_listener = MyListener()

    connection = leap.Connection()
    connection.add_listener(my_listener)

    running = True

    with connection.open():
        connection.set_tracking_mode(leap.TrackingMode.Desktop)
        while running:
            for hand in my_listener.hands:
                hand_data["left" if hand.type == leap.HandType.Left else "right"] = {
                    "palm": {
                        "x": hand.palm.position.x,
                        "y": hand.palm.position.y,
                        "z": hand.palm.position.z
                    },
                }
                for i,j in zip(digits, hand.digits):
                    hand_data["left" if hand.type == leap.HandType.Left else "right"][i] ={}
                    for k, l in zip(bones, j.bones):
                        hand_data["left" if hand.type == leap.HandType.Left else "right"][i][k] = {
                            "width": l.width,
                            "x": l.rotation.x,
                            "y": l.rotation.y,
                            "z": l.rotation.z,
                            "w": l.rotation.w
                        }
                hand_data["left" if hand.type == leap.HandType.Left else "right"]["arm"] = {
                    "width": hand.arm.width,
                    "x": hand.arm.rotation.x,
                    "y": hand.arm.rotation.y,
                    "z": hand.arm.rotation.z,
                    "w": hand.arm.rotation.w
                }
            print(hand_data)
            time.sleep(1/hz)

initialise_leapmotion(5)