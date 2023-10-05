import math

def calc_distance(curr_loc, goal_loc):
    # For Normal, IL
    # 1 degree of latitude = ~111 km (x component)
    # 1 degree of longitude = ~89 km (y compoenent)
    curr_x = float(curr_loc.split(',')[0])*89
    curr_y = float(curr_loc.split(',')[1])*111
    goal_x = float(goal_loc.split(',')[0])*89
    goal_y = float(goal_loc.split(',')[1])*111
    dist = math.sqrt((goal_x - curr_x)**2 + (goal_y - curr_y)**2)
    dist = round(dist*1000) # Convert to Meters
    return dist

def calc_time(dist, speed):
    # Speed is in meters per minute
    # Time is in minutes
    time = dist/speed
    return time