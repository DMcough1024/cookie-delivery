import datetime
import os
import calculator as c
dir_path = os.path.dirname(os.path.realpath(__file__))
stores = c.read_address_file(os.path.join(dir_path, "stores.txt")) # easier to import this again here since stores don't change often.

def time_marches_on(ct, adv_time, drones, orders):
    global current_time 
    current_time = ct + datetime.timedelta(minutes=adv_time)

    # check if any drones are arriving at their destination
    for d in drones:
        orders = d.check(orders, current_time)
        d.move(adv_time, current_time)
    
    # check if any orders are in need of a drone
    for o in orders:
        if o.delivered_by == "":
            print("New order: ")
            c.print_an_order(o)
            del_drone, drones, orders = assign_drone(o, drones, orders)
            o.delivered_by = del_drone.name
            print("Order " + str(o.id) + " is assigned to " + o.delivered_by + ".")

    return current_time, drones, orders

def assign_drone(order, drones, orders):
    fastest_drone = ""
    time_to_delivery = ""

    # loop through the drones, calculate the time to delivery for each drone
    for d in drones: 
        if d.free_at <= current_time:
            ttf = 0
            start_loc = d.location
        else:
            ttf = (d.free_at - current_time).total_seconds()/60
            if len(d.order_id) <= 1:
                start_loc = d.going_to
            else:
                start_loc = orders[d.order_id[-1]].location

        # now that we know how long it is until the drone is available, we check the time the drone will take to deliver the order
        via, route_time = plan_route(start_loc, order.location, d.speed)
        total_time = ttf + route_time

        # with total time calculated, we can compare it to the current fastest drone, and continue the loop
        if fastest_drone == "" or total_time < time_to_delivery:
            fastest_drone = d
            time_to_delivery = total_time
    
    # We have found the fasted drone, now we assign the order to it
    print("Fastest Drone: " + fastest_drone.name)
    fastest_drone, order = fastest_drone.assign(order, current_time)
    drones[drones.index(fastest_drone)] = fastest_drone
    
    return fastest_drone, drones, orders

def plan_route(curr_loc, goal_loc, speed):
    # Drone must go from curr_loc to goal_loc via 1 store
    drone_to_store = {}
    goal_to_store = {}
    for s in stores:
        dist_drone = c.calc_distance(curr_loc, stores[s]) 
        dist_goal = c.calc_distance(stores[s], goal_loc)
        drone_to_store[s] = dist_drone
        goal_to_store[s] = dist_goal

    # find the shortest distance from curr_loc to goal_loc via 1 store
    via = ""
    shortest_dist = ""
    for s in stores:
        if via == "" or (drone_to_store[s] + goal_to_store[s]) < shortest_dist:
            via = s
            shortest_dist = drone_to_store[s] + goal_to_store[s]

    # return the store object and the time the route will take
    route_time = c.calc_time(shortest_dist, speed)
    return via, route_time