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
    time = dist/speed
    return time

def calc_move(curr_loc, goal_loc, dist):
    # given two cardinal points (curr_loc and goal_loc)
    # and given a distance, calculate the new location
    curr_x = float(curr_loc.split(',')[0])
    curr_y = float(curr_loc.split(',')[1])
    goal_x = float(goal_loc.split(',')[0])
    goal_y = float(goal_loc.split(',')[1])
    full_dist = calc_distance(curr_loc, goal_loc)
    ratio = dist/full_dist
    if dist > full_dist:
        new_loc = goal_loc
    else:
        if curr_x > goal_x:
            new_x = curr_x - (ratio * abs(curr_x - goal_x))
        else:
            new_x = curr_x + (ratio * abs(curr_x - goal_x))
        if curr_y > goal_y:
            new_y = curr_y - (ratio * abs(curr_y - goal_y))
        else:
            new_y = curr_y + (ratio * abs(curr_y - goal_y))
        new_loc = str(new_x) + ',' + str(new_y)
    
    return new_loc 

def read_address_file(filename):
    # Read the .txt files that contain addresses and co-ordinates and return a dictionary
    with open(filename, 'r') as file:
        addy = {}
        for line in file:
            key, value = line.strip().split(':')
            addy[key] = value
    return addy

def print_an_order(o):
    # print out all the details of a single order
    print("Order ID: " + str(o.id))
    print("Address: " + o.address)
    print("Ordered at: " + str(o.ordered_at))
    print("Location: " + str(o.location))
    print("Delivered by: " + str(o.delivered_by))
    print("Fulfilled by: " + str(o.fulfilled_by))
    print("Fulfilled at: " + str(o.fulfilled_at))
    print("")
    return

def print_a_drone(d):
    # print out all the details of a single drone
    print("ID: " + str(d.id))
    print("Name: " + d.name)
    print("Home: " + d.home)
    print("Free at: " + str(d.free_at))
    print("Arriving at: " + str(d.arriving_at))
    print("Order ID: " + str(d.order_id))
    print("Location: " + str(d.location))
    print("Going to: " + str(d.going_to))
    print("Speed: " + str(d.speed))
    print("")
    return