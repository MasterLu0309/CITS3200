import polhemus
import time


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
                "AngleZ2": tracker_list[i].AngleZ2
            }
    return data

def close_trackers(tracker_list: list):
    """
    Closes provided list of tracker objects.
    """
    for i in range(len(tracker_list)):
        tracker_list[i].Close()


if __name__ == "__main__":
    trackers = initialise_polhemus(1)
    with open("test_output.csv", "w") as file:
        while True:
            data = get_polhemus_data(trackers, False)
            print(data)
            file.write(str(data) + "\n")
            time.sleep(0.1)