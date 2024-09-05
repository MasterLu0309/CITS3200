import polhemus
import time

# Requires Polhemus Liberty USB driver to be installed for communication
# https://ftp.polhemus1.com/pub/Trackers/Liberty/
# WARNING: Above driver is NOT COMPATIBLE with Windows 11's 'Core Isolation' security feature.

another = False

def initialise_polhemus(amount: int) -> list:
    """
    Takes in an 'int' amount of polhemus trackers to initialise and returns a list of all the tracker objects.
    """
    tracker_list = [None]*amount
    for i in range(amount):
        tracker_list[i] = polhemus.polhemus()
        tracker_list[i].Initialize()
    return tracker_list

def get_polhemus_data(tracker_list: list, stylus: bool) -> list[dict]:
    """
    Takes in list of tracker objects, reads the data from each tracker, and returns a list of dictionaries containing
    the data for each tracker. 
    """
    tracker_amount = len(tracker_list)
    data = [None]*tracker_amount
    for i in range(tracker_amount):
        tracker_list[i].Run() # This method seems to not initialise the tracker, but rather read in the data from it.
        timestamp = time.time()
        if stylus:
            data[i] = {
                "Timestamp": timestamp,
                "PositionX1": tracker_list[i].PositionTooltipX1,
                "PositionY1": tracker_list[i].PositionTooltipY1,
                "PositionZ1": tracker_list[i].PositionTooltipZ1,
                "AngleX1": tracker_list[i].AngleX1,
                "AngleY1": tracker_list[i].AngleY1,
                "AngleZ1": tracker_list[i].AngleZ1,
                "PositionX2": tracker_list[i].PositionTooltipX2,
                "PositionY2": tracker_list[i].PositionTooltipY2,
                "PositionZ2": tracker_list[i].PositionTooltipZ2,
                "AngleX2": tracker_list[i].AngleX2,
                "AngleY2": tracker_list[i].AngleY2,
                "AngleZ2": tracker_list[i].AngleZ2,
                "StylusButton": tracker_list[i].StylusButton,
                "Sensor1": tracker_list[i].Sensor1,
                "Sensor2": tracker_list[i].Sensor2
            }
        else:
            data[i] = {
                "Timestamp": timestamp,
                "PositionX1": tracker_list[i].PositionTooltipX1,
                "PositionY1": tracker_list[i].PositionTooltipY1,
                "PositionZ1": tracker_list[i].PositionTooltipZ1,
                "AngleX1": tracker_list[i].AngleX1,
                "AngleY1": tracker_list[i].AngleY1,
                "AngleZ1": tracker_list[i].AngleZ1,
                "PositionX2": tracker_list[i].PositionTooltipX2,
                "PositionY2": tracker_list[i].PositionTooltipY2,
                "PositionZ2": tracker_list[i].PositionTooltipZ2,
                "AngleX2": tracker_list[i].AngleX2,
                "AngleY2": tracker_list[i].AngleY2,
                "AngleZ2": tracker_list[i].AngleZ2,
                "StylusButton": 0,
                "Sensor1": 0,
                "Sensor2": 0
            }
    return data

def close_trackers(tracker_list: list):
    """
    Closes provided list of tracker objects.
    """
    for i in range(len(tracker_list)):
        tracker_list[i].Close()

def output_data(hz: int):
    global another
    another = True

    trackers = initialise_polhemus(1)
    with open("polhemus_output.csv", "w") as file:
        file.write("Timestamp,PositionX1,PositionY1,PositionZ1,AngleX1,AngleY1,AngleZ1,PositionX2,PositionY2,PositionZ2,AngleX2,AngleY2,AngleZ2,StylusButton,Sensor1,Sensor2\n")
        while another:
            data = get_polhemus_data(trackers, False)
            current_data = f"{data[0]['Timestamp']},{data[0]['PositionX1']},{data[0]['PositionY1']},{data[0]['PositionZ1']},{data[0]['AngleX1']},{data[0]['AngleY1']},{data[0]['AngleZ1']},{data[0]['PositionX2']},{data[0]['PositionY2']},{data[0]['PositionZ2']},{data[0]['AngleX2']},{data[0]['AngleY2']},{data[0]['AngleZ2']},0,0,0"
            print(current_data)
            file.write(current_data + "\n")
            time.sleep(1/hz)