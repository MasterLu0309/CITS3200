import polhemus

'''
Takes in an 'int' amount of polhemus trackers to initialise and returns a list of all the tracker objects.
'''
def initialise_all_trackers(amount: int) -> list:
    tracker_list = [None]*amount
    for i in range(amount):
        tracker_list[i] = polhemus.polhemus()
        tracker_list[i].Initialize()
        tracker_list[i].Run()
    return tracker_list
