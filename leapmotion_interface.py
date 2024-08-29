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
        hands_data = {}
        for hand in event.hands:
            hands_data[hand.id] = {
                "type": "left" if str(hand.type) == "HandType.Left" else "right",
                "palm_position": {
                    "x": hand.palm.position.x,
                    "y": hand.palm.position.y,
                    "z": hand.palm.position.z
                },
                "digits": {
                    "thumb": {
                        "id": hand.thumb.finger_id,
                        "metacarpal": {
                            "width": hand.thumb.metacarpal.width,
                            "position": {
                                "x": hand.thumb.metacarpal.rotation.x,
                                "y": hand.thumb.metacarpal.rotation.y,
                                "z": hand.thumb.metacarpal.rotation.z,
                                "w": hand.thumb.metacarpal.rotation.w
                            }
                        }
                    },
                    "index": {
                        "id": hand.index.finger_id,
                        "metacarpal": {
                            "width": hand.index.metacarpal.width,
                            "position": {
                                "x": hand.index.metacarpal.rotation.x,
                                "y": hand.index.metacarpal.rotation.y,
                                "z": hand.index.metacarpal.rotation.z,
                                "w": hand.index.metacarpal.rotation.w
                            }
                        }
                    },
                    "middle": {
                        "id": hand.middle.finger_id,
                        "metacarpal": {
                            "width": hand.middle.metacarpal.width,
                            "position": {
                                "x": hand.middle.metacarpal.rotation.x,
                                "y": hand.middle.metacarpal.rotation.y,
                                "z": hand.middle.metacarpal.rotation.z,
                                "w": hand.middle.metacarpal.rotation.w
                            }
                        }
                    },
                    "ring": {
                        "id": hand.ring.finger_id,
                        "metacarpal": {
                            "width": hand.ring.metacarpal.width,
                            "position": {
                                "x": hand.ring.metacarpal.rotation.x,
                                "y": hand.ring.metacarpal.rotation.y,
                                "z": hand.ring.metacarpal.rotation.z,
                                "w": hand.ring.metacarpal.rotation.w
                            }
                        }
                    },
                    "pinky": {
                        "id": hand.pinky.finger_id,
                        "metacarpal": {
                            "width": hand.pinky.metacarpal.width,
                            "position": {
                                "x": hand.pinky.metacarpal.rotation.x,
                                "y": hand.pinky.metacarpal.rotation.y,
                                "z": hand.pinky.metacarpal.rotation.z,
                                "w": hand.pinky.metacarpal.rotation.w
                            }
                        }
                    }
                },
                "arm": {
                    "width": hand.arm.width,
                    "position": {
                        "x": hand.arm.rotation.x,
                        "y": hand.arm.rotation.y,
                        "z": hand.arm.rotation.z,
                        "w": hand.arm.rotation.w
                    }
                }
            }
            
            print(hands_data)

if __name__ == "__main__":
    my_listener = MyListener()

    connection = leap.Connection()
    connection.add_listener(my_listener)

    running = True

    with connection.open():
        connection.set_tracking_mode(leap.TrackingMode.Desktop)
        while running:
            time.sleep(1)