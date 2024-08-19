import polhemus

'''
Takes in an 'int' amount of polhemus trackers to initialise and returns a list of all the tracker objects.
'''
def initialise_trackers(amount: int) -> list:
    tracker_list = [None]*amount
    for i in range(amount):
        tracker_list[i] = polhemus.polhemus()
        tracker_list[i].Initialize()
        tracker_list[i].Run()
    return tracker_list

'''
Takes in list of tracker objects, reads the data from each tracker, and returns a list of dictionaries containing
the data for each tracker. 
'''
def get_tracker_data(tracker_list: list) -> list[dict]:
    tracker_amount = len(tracker_list)
    data = [None]*tracker_amount
    for i in range(tracker_amount):
        data[i] = {
            "PositionTooltipX1": tracker_list[i].PositionTooltipX1,
            "PositionTooltipY1": tracker_list[i].PositionTooltipY1,
            "PositionTooltipZ1": tracker_list[i].PositionTooltipZ1,
            "AngleX1": tracker_list[i].AngleX1,
            "AngleY1": tracker_list[i].AngleY1,
            "AngleZ1": tracker_list[i].AngleZ1,
            "PositionTooltipX2": tracker_list[i].PositionTooltipX2,
            "PositionTooltipY2": tracker_list[i].PositionTooltipY2,
            "PositionTooltipZ2": tracker_list[i].PositionTooltipZ2,
            "AngleX2": tracker_list[i].AngleX2,
            "AngleY2": tracker_list[i].AngleY2,
            "AngleZ2": tracker_list[i].AngleZ2,
            "StylusButton": tracker_list[i].StylusButton,
            "Sensor1": tracker_list[i].Sensor1,
            "Sensor2": tracker_list[i].Sensor2
        }
    return data


'''
Closes provided list of tracker objects.
'''
def close_trackers(tracker_list: list):
    for i in range(len(tracker_list)):
        tracker_list[i].Close()