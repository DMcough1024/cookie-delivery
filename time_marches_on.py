import datetime

def time_marches_on(current_time, adv_time):
    current_time = current_time + datetime.timedelta(minutes=adv_time)
    return current_time


def time_to_coor(curr_loc, goal_loc, speed):
    # Calculate the distance between the two points
    # Calculate the time to travel that distance
    # Return the time
    # curr_loc and goal_loc are tuples of (lat, long)
    # speed is in mph
    # For small city assume lat / long are square grid. 
    print(curr_loc)
    print(goal_loc)
    time = 0
    return time