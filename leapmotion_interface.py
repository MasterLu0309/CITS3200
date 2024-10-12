import leap
import time
import json

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

# This code is based on the LeapC API, which is a C API. The Leap Python API is a wrapper around this C API.

# Global variable to stop the polling and output of Leapmotion data,
# setting this at any time to False will stop output. Must be set to
# True for output to occur.
another = True
connection = None

# These are the same three modes that can be seen in the Leapmotion Control Panel.
tracking_modes = {
    "Desktop": leap.TrackingMode.Desktop,
    "Head Mounted": leap.TrackingMode.HMD,
    "Screentop": leap.TrackingMode.ScreenTop
}

SELECTED_MODE = None

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

    def is_hand(self):
        return len(self.hands) > 0


def initialise_leapmotion(hz: int):
    hand_data = {}
    # Each hand has these digits, each digit having each of thes bones
    digits = ["thumb", "index", "middle", "ring", "pinky"]
    bones = ["metacarpal", "proximal", "intermediate", "distal"]
    my_listener = MyListener()

    global connection
    connection = leap.Connection()
    connection.add_listener(my_listener)

    running = True
    #217 columns
    headers = "Timestamp,LeftPalmX,LeftPalmY,LeftPalmZ,LeftThumbMetacarpalWidth,LeftThumbMetacarpalX,LeftThumbMetacarpalY,LeftThumbMetacarpalZ,LeftThumbMetacarpalW,LeftThumbProximalWidth,LeftThumbProximalX,LeftThumbProximalY,LeftThumbProximalZ,LeftThumbProximalW,LeftThumbIntermediateWidth,LeftThumbIntermediateX,LeftThumbIntermediateY,LeftThumbIntermediateZ,LeftThumbIntermediateW,LeftThumbDistalWidth,LeftThumbDistalX,LeftThumbDistalY,LeftThumbDistalZ,LeftThumbDistalW,LeftIndexMetacarpalWidth,LeftIndexMetacarpalX,LeftIndexMetacarpalY,LeftIndexMetacarpalZ,LeftIndexMetacarpalW,LeftIndexProximalWidth,LeftIndexProximalX,LeftIndexProximalY,LeftIndexProximalZ,LeftIndexProximalW,LeftIndexIntermediateWidth,LeftIndexIntermediateX,LeftIndexIntermediateY,LeftIndexIntermediateZ,LeftIndexIntermediateW,LeftIndexDistalWidth,LeftIndexDistalX,LeftIndexDistalY,LeftIndexDistalZ,LeftIndexDistalW,LeftMiddleMetacarpalWidth,LeftMiddleMetacarpalX,LeftMiddleMetacarpalY,LeftMiddleMetacarpalZ,LeftMiddleMetacarpalW,LeftMiddleProximalWidth,LeftMiddleProximalX,LeftMiddleProximalY,LeftMiddleProximalZ,LeftMiddleProximalW,LeftMiddleIntermediateWidth,LeftMiddleIntermediateX,LeftMiddleIntermediateY,LeftMiddleIntermediateZ,LeftMiddleIntermediateW,LeftMiddleDistalWidth,LeftMiddleDistalX,LeftMiddleDistalY,LeftMiddleDistalZ,LeftMiddleDistalW,LeftRingMetacarpalWidth,LeftRingMetacarpalX,LeftRingMetacarpalY,LeftRingMetacarpalZ,LeftRingMetacarpalW,LeftRingProximalWidth,LeftRingProximalX,LeftRingProximalY,LeftRingProximalZ,LeftRingProximalW,LeftRingIntermediateWidth,LeftRingIntermediateX,LeftRingIntermediateY,LeftRingIntermediateZ,LeftRingIntermediateW,LeftRingDistalWidth,LeftRingDistalX,LeftRingDistalY,LeftRingDistalZ,LeftRingDistalW,LeftPinkyMetacarpalWidth,LeftPinkyMetacarpalX,LeftPinkyMetacarpalY,LeftPinkyMetacarpalZ,LeftPinkyMetacarpalW,LeftPinkyProximalWidth,LeftPinkyProximalX,LeftPinkyProximalY,LeftPinkyProximalZ,LeftPinkyProximalW,LeftPinkyIntermediateWidth,LeftPinkyIntermediateX,LeftPinkyIntermediateY,LeftPinkyIntermediateZ,LeftPinkyIntermediateW,LeftPinkyDistalWidth,LeftPinkyDistalX,LeftPinkyDistalY,LeftPinkyDistalZ,LeftPinkyDistalW,LeftArmWidth,LeftArmX,LeftArmY,LeftArmZ,LeftArmW,RightPalmX,RightPalmY,RightPalmZ,RightThumbMetacarpalWidth,RightThumbMetacarpalX,RightThumbMetacarpalY,RightThumbMetacarpalZ,RightThumbMetacarpalW,RightThumbProximalWidth,RightThumbProximalX,RightThumbProximalY,RightThumbProximalZ,RightThumbProximalW,RightThumbIntermediateWidth,RightThumbIntermediateX,RightThumbIntermediateY,RightThumbIntermediateZ,RightThumbIntermediateW,RightThumbDistalWidth,RightThumbDistalX,RightThumbDistalY,RightThumbDistalZ,RightThumbDistalW,RightIndexMetacarpalWidth,RightIndexMetacarpalX,RightIndexMetacarpalY,RightIndexMetacarpalZ,RightIndexMetacarpalW,RightIndexProximalWidth,RightIndexProximalX,RightIndexProximalY,RightIndexProximalZ,RightIndexProximalW,RightIndexIntermediateWidth,RightIndexIntermediateX,RightIndexIntermediateY,RightIndexIntermediateZ,RightIndexIntermediateW,RightIndexDistalWidth,RightIndexDistalX,RightIndexDistalY,RightIndexDistalZ,RightIndexDistalW,RightMiddleMetacarpalWidth,RightMiddleMetacarpalX,RightMiddleMetacarpalY,RightMiddleMetacarpalZ,RightMiddleMetacarpalW,RightMiddleProximalWidth,RightMiddleProximalX,RightMiddleProximalY,RightMiddleProximalZ,RightMiddleProximalW,RightMiddleIntermediateWidth,RightMiddleIntermediateX,RightMiddleIntermediateY,RightMiddleIntermediateZ,RightMiddleIntermediateW,RightMiddleDistalWidth,RightMiddleDistalX,RightMiddleDistalY,RightMiddleDistalZ,RightMiddleDistalW,RightRingMetacarpalWidth,RightRingMetacarpalX,RightRingMetacarpalY,RightRingMetacarpalZ,RightRingMetacarpalW,RightRingProximalWidth,RightRingProximalX,RightRingProximalY,RightRingProximalZ,RightRingProximalW,RightRingIntermediateWidth,RightRingIntermediateX,RightRingIntermediateY,RightRingIntermediateZ,RightRingIntermediateW,RightRingDistalWidth,RightRingDistalX,RightRingDistalY,RightRingDistalZ,RightRingDistalW,RightPinkyMetacarpalWidth,RightPinkyMetacarpalX,RightPinkyMetacarpalY,RightPinkyMetacarpalZ,RightPinkyMetacarpalW,RightPinkyProximalWidth,RightPinkyProximalX,RightPinkyProximalY,RightPinkyProximalZ,RightPinkyProximalW,RightPinkyIntermediateWidth,RightPinkyIntermediateX,RightPinkyIntermediateY,RightPinkyIntermediateZ,RightPinkyIntermediateW,RightPinkyDistalWidth,RightPinkyDistalX,RightPinkyDistalY,RightPinkyDistalZ,RightPinkyDistalW,RightArmWidth,RightArmX,RightArmY,RightArmZ,RightArmW"
    with open("leapmotion_output.csv", "w") as file:
        file.write(headers)
        file.write("\n")
        with connection.open():
            connection.set_tracking_mode(SELECTED_MODE)
            while running:
                # if my_listener.is_hand():
                #     print("Hand detected")
                # else:
                #     print("No hand detected")
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
                if another:
                    #print(hand_data)
                    file.write(f'{time.time()},')
                    if my_listener.is_hand():
                        try:
                            file.write(f'{hand_data["left"]["palm"]["x"]},{hand_data["left"]["palm"]["y"]},{hand_data["left"]["palm"]["z"]},{hand_data["left"]["thumb"]["metacarpal"]["width"]},{hand_data["left"]["thumb"]["metacarpal"]["x"]},{hand_data["left"]["thumb"]["metacarpal"]["y"]},{hand_data["left"]["thumb"]["metacarpal"]["z"]},{hand_data["left"]["thumb"]["metacarpal"]["w"]},{hand_data["left"]["thumb"]["proximal"]["width"]},{hand_data["left"]["thumb"]["proximal"]["x"]},{hand_data["left"]["thumb"]["proximal"]["y"]},{hand_data["left"]["thumb"]["proximal"]["z"]},{hand_data["left"]["thumb"]["proximal"]["w"]},{hand_data["left"]["thumb"]["intermediate"]["width"]},{hand_data["left"]["thumb"]["intermediate"]["x"]},{hand_data["left"]["thumb"]["intermediate"]["y"]},{hand_data["left"]["thumb"]["intermediate"]["z"]},{hand_data["left"]["thumb"]["intermediate"]["w"]},{hand_data["left"]["thumb"]["distal"]["width"]},{hand_data["left"]["thumb"]["distal"]["x"]},{hand_data["left"]["thumb"]["distal"]["y"]},{hand_data["left"]["thumb"]["distal"]["z"]},{hand_data["left"]["thumb"]["distal"]["w"]},{hand_data["left"]["index"]["metacarpal"]["width"]},{hand_data["left"]["index"]["metacarpal"]["x"]},{hand_data["left"]["index"]["metacarpal"]["y"]},{hand_data["left"]["index"]["metacarpal"]["z"]},{hand_data["left"]["index"]["metacarpal"]["w"]},{hand_data["left"]["index"]["proximal"]["width"]},{hand_data["left"]["index"]["proximal"]["x"]},{hand_data["left"]["index"]["proximal"]["y"]},{hand_data["left"]["index"]["proximal"]["z"]},{hand_data["left"]["index"]["proximal"]["w"]},{hand_data["left"]["index"]["intermediate"]["width"]},{hand_data["left"]["index"]["intermediate"]["x"]},{hand_data["left"]["index"]["intermediate"]["y"]},{hand_data["left"]["index"]["intermediate"]["z"]},{hand_data["left"]["index"]["intermediate"]["w"]},{hand_data["left"]["index"]["distal"]["width"]},{hand_data["left"]["index"]["distal"]["x"]},{hand_data["left"]["index"]["distal"]["y"]},{hand_data["left"]["index"]["distal"]["z"]},{hand_data["left"]["index"]["distal"]["w"]},{hand_data["left"]["middle"]["metacarpal"]["width"]},{hand_data["left"]["middle"]["metacarpal"]["x"]},{hand_data["left"]["middle"]["metacarpal"]["y"]},{hand_data["left"]["middle"]["metacarpal"]["z"]},{hand_data["left"]["middle"]["metacarpal"]["w"]},{hand_data["left"]["middle"]["proximal"]["width"]},{hand_data["left"]["middle"]["proximal"]["x"]},{hand_data["left"]["middle"]["proximal"]["y"]},{hand_data["left"]["middle"]["proximal"]["z"]},{hand_data["left"]["middle"]["proximal"]["w"]},{hand_data["left"]["middle"]["intermediate"]["width"]},{hand_data["left"]["middle"]["intermediate"]["x"]},{hand_data["left"]["middle"]["intermediate"]["y"]},{hand_data["left"]["middle"]["intermediate"]["z"]},{hand_data["left"]["middle"]["intermediate"]["w"]},{hand_data["left"]["middle"]["distal"]["width"]},{hand_data["left"]["middle"]["distal"]["x"]},{hand_data["left"]["middle"]["distal"]["y"]},{hand_data["left"]["middle"]["distal"]["z"]},{hand_data["left"]["middle"]["distal"]["w"]},{hand_data["left"]["ring"]["metacarpal"]["width"]},{hand_data["left"]["ring"]["metacarpal"]["x"]},{hand_data["left"]["ring"]["metacarpal"]["y"]},{hand_data["left"]["ring"]["metacarpal"]["z"]},{hand_data["left"]["ring"]["metacarpal"]["w"]},{hand_data["left"]["ring"]["proximal"]["width"]},{hand_data["left"]["ring"]["proximal"]["x"]},{hand_data["left"]["ring"]["proximal"]["y"]},{hand_data["left"]["ring"]["proximal"]["z"]},{hand_data["left"]["ring"]["proximal"]["w"]},{hand_data["left"]["ring"]["intermediate"]["width"]},{hand_data["left"]["ring"]["intermediate"]["x"]},{hand_data["left"]["ring"]["intermediate"]["y"]},{hand_data["left"]["ring"]["intermediate"]["z"]},{hand_data["left"]["ring"]["intermediate"]["w"]},{hand_data["left"]["ring"]["distal"]["width"]},{hand_data["left"]["ring"]["distal"]["x"]},{hand_data["left"]["ring"]["distal"]["y"]},{hand_data["left"]["ring"]["distal"]["z"]},{hand_data["left"]["ring"]["distal"]["w"]},{hand_data["left"]["pinky"]["metacarpal"]["width"]},{hand_data["left"]["pinky"]["metacarpal"]["x"]},{hand_data["left"]["pinky"]["metacarpal"]["y"]},{hand_data["left"]["pinky"]["metacarpal"]["z"]},{hand_data["left"]["pinky"]["metacarpal"]["w"]},{hand_data["left"]["pinky"]["proximal"]["width"]},{hand_data["left"]["pinky"]["proximal"]["x"]},{hand_data["left"]["pinky"]["proximal"]["y"]},{hand_data["left"]["pinky"]["proximal"]["z"]},{hand_data["left"]["pinky"]["proximal"]["w"]},{hand_data["left"]["pinky"]["intermediate"]["width"]},{hand_data["left"]["pinky"]["intermediate"]["x"]},{hand_data["left"]["pinky"]["intermediate"]["y"]},{hand_data["left"]["pinky"]["intermediate"]["z"]},{hand_data["left"]["pinky"]["intermediate"]["w"]},{hand_data["left"]["pinky"]["distal"]["width"]},{hand_data["left"]["pinky"]["distal"]["x"]},{hand_data["left"]["pinky"]["distal"]["y"]},{hand_data["left"]["pinky"]["distal"]["z"]},{hand_data["left"]["pinky"]["distal"]["w"]},{hand_data["left"]["arm"]["width"]},{hand_data["left"]["arm"]["x"]},{hand_data["left"]["arm"]["y"]},{hand_data["left"]["arm"]["z"]},{hand_data["left"]["arm"]["w"]}')
                        except KeyError:
                            file.write(','*108)
                        try:
                            file.write(f',{hand_data["right"]["palm"]["x"]},{hand_data["right"]["palm"]["y"]},{hand_data["right"]["palm"]["z"]},{hand_data["right"]["thumb"]["metacarpal"]["width"]},{hand_data["right"]["thumb"]["metacarpal"]["x"]},{hand_data["right"]["thumb"]["metacarpal"]["y"]},{hand_data["right"]["thumb"]["metacarpal"]["z"]},{hand_data["right"]["thumb"]["metacarpal"]["w"]},{hand_data["right"]["thumb"]["proximal"]["width"]},{hand_data["right"]["thumb"]["proximal"]["x"]},{hand_data["right"]["thumb"]["proximal"]["y"]},{hand_data["right"]["thumb"]["proximal"]["z"]},{hand_data["right"]["thumb"]["proximal"]["w"]},{hand_data["right"]["thumb"]["intermediate"]["width"]},{hand_data["right"]["thumb"]["intermediate"]["x"]},{hand_data["right"]["thumb"]["intermediate"]["y"]},{hand_data["right"]["thumb"]["intermediate"]["z"]},{hand_data["right"]["thumb"]["intermediate"]["w"]},{hand_data["right"]["thumb"]["distal"]["width"]},{hand_data["right"]["thumb"]["distal"]["x"]},{hand_data["right"]["thumb"]["distal"]["y"]},{hand_data["right"]["thumb"]["distal"]["z"]},{hand_data["right"]["thumb"]["distal"]["w"]},{hand_data["right"]["index"]["metacarpal"]["width"]},{hand_data["right"]["index"]["metacarpal"]["x"]},{hand_data["right"]["index"]["metacarpal"]["y"]},{hand_data["right"]["index"]["metacarpal"]["z"]},{hand_data["right"]["index"]["metacarpal"]["w"]},{hand_data["right"]["index"]["proximal"]["width"]},{hand_data["right"]["index"]["proximal"]["x"]},{hand_data["right"]["index"]["proximal"]["y"]},{hand_data["right"]["index"]["proximal"]["z"]},{hand_data["right"]["index"]["proximal"]["w"]},{hand_data["right"]["index"]["intermediate"]["width"]},{hand_data["right"]["index"]["intermediate"]["x"]},{hand_data["right"]["index"]["intermediate"]["y"]},{hand_data["right"]["index"]["intermediate"]["z"]},{hand_data["right"]["index"]["intermediate"]["w"]},{hand_data["right"]["index"]["distal"]["width"]},{hand_data["right"]["index"]["distal"]["x"]},{hand_data["right"]["index"]["distal"]["y"]},{hand_data["right"]["index"]["distal"]["z"]},{hand_data["right"]["index"]["distal"]["w"]},{hand_data["right"]["middle"]["metacarpal"]["width"]},{hand_data["right"]["middle"]["metacarpal"]["x"]},{hand_data["right"]["middle"]["metacarpal"]["y"]},{hand_data["right"]["middle"]["metacarpal"]["z"]},{hand_data["right"]["middle"]["metacarpal"]["w"]},{hand_data["right"]["middle"]["proximal"]["width"]},{hand_data["right"]["middle"]["proximal"]["x"]},{hand_data["right"]["middle"]["proximal"]["y"]},{hand_data["right"]["middle"]["proximal"]["z"]},{hand_data["right"]["middle"]["proximal"]["w"]},{hand_data["right"]["middle"]["intermediate"]["width"]},{hand_data["right"]["middle"]["intermediate"]["x"]},{hand_data["right"]["middle"]["intermediate"]["y"]},{hand_data["right"]["middle"]["intermediate"]["z"]},{hand_data["right"]["middle"]["intermediate"]["w"]},{hand_data["right"]["middle"]["distal"]["width"]},{hand_data["right"]["middle"]["distal"]["x"]},{hand_data["right"]["middle"]["distal"]["y"]},{hand_data["right"]["middle"]["distal"]["z"]},{hand_data["right"]["middle"]["distal"]["w"]},{hand_data["right"]["ring"]["metacarpal"]["width"]},{hand_data["right"]["ring"]["metacarpal"]["x"]},{hand_data["right"]["ring"]["metacarpal"]["y"]},{hand_data["right"]["ring"]["metacarpal"]["z"]},{hand_data["right"]["ring"]["metacarpal"]["w"]},{hand_data["right"]["ring"]["proximal"]["width"]},{hand_data["right"]["ring"]["proximal"]["x"]},{hand_data["right"]["ring"]["proximal"]["y"]},{hand_data["right"]["ring"]["proximal"]["z"]},{hand_data["right"]["ring"]["proximal"]["w"]},{hand_data["right"]["ring"]["intermediate"]["width"]},{hand_data["right"]["ring"]["intermediate"]["x"]},{hand_data["right"]["ring"]["intermediate"]["y"]},{hand_data["right"]["ring"]["intermediate"]["z"]},{hand_data["right"]["ring"]["intermediate"]["w"]},{hand_data["right"]["ring"]["distal"]["width"]},{hand_data["right"]["ring"]["distal"]["x"]},{hand_data["right"]["ring"]["distal"]["y"]},{hand_data["right"]["ring"]["distal"]["z"]},{hand_data["right"]["ring"]["distal"]["w"]},{hand_data["right"]["pinky"]["metacarpal"]["width"]},{hand_data["right"]["pinky"]["metacarpal"]["x"]},{hand_data["right"]["pinky"]["metacarpal"]["y"]},{hand_data["right"]["pinky"]["metacarpal"]["z"]},{hand_data["right"]["pinky"]["metacarpal"]["w"]},{hand_data["right"]["pinky"]["proximal"]["width"]},{hand_data["right"]["pinky"]["proximal"]["x"]},{hand_data["right"]["pinky"]["proximal"]["y"]},{hand_data["right"]["pinky"]["proximal"]["z"]},{hand_data["right"]["pinky"]["proximal"]["w"]},{hand_data["right"]["pinky"]["intermediate"]["width"]},{hand_data["right"]["pinky"]["intermediate"]["x"]},{hand_data["right"]["pinky"]["intermediate"]["y"]},{hand_data["right"]["pinky"]["intermediate"]["z"]},{hand_data["right"]["pinky"]["intermediate"]["w"]},{hand_data["right"]["pinky"]["distal"]["width"]},{hand_data["right"]["pinky"]["distal"]["x"]},{hand_data["right"]["pinky"]["distal"]["y"]},{hand_data["right"]["pinky"]["distal"]["z"]},{hand_data["right"]["pinky"]["distal"]["w"]},{hand_data["right"]["arm"]["width"]},{hand_data["right"]["arm"]["x"]},{hand_data["right"]["arm"]["y"]},{hand_data["right"]["arm"]["z"]},{hand_data["right"]["arm"]["w"]}\n')
                        except KeyError:
                            file.write(','*108)
                            file.write('\n')
                    else:
                        file.write('\n')
                time.sleep(1/hz)