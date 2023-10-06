# This program will manage the cookie delivery drones for a fictional city.

# Import the necessary modules 
import os
import random
import datetime 
import math
import traceback
import current_map as map
import time_marches_on as march
import calculator as c

# Global variables
global id
global d_id
global current_time
id = 0
d_id = 0
current_time = datetime.datetime.now()
current_time = current_time.replace(second=0, microsecond=0)
orders = []
drones = []

# Define classes
class Drone:
    def __init__(self, name, store, ct=current_time):
        self.id = d_id
        self.name = name
        self.home = store
        self.home_loc = stores[store]
        self.going_to = stores[store]
        self.arriving_at = ct
        self.free_at = ct
        self.order_id = []
        self.location = stores[store]
        self.speed = 500 # meters per minute, over-written in main
    
    def check(self, orders, ct=current_time):
        print("")
        if ct > self.arriving_at and len(self.order_id) > 0:
            print("Drone " + self.name + " delivered order " + str(self.order_id[0]))
            self.deliver(self.order_id[0], ct)
        elif ct > self.arriving_at and len(self.order_id) == 0:
            self.location = self.home_loc
            print("Drone " + self.name + " is home.")
        elif ct < self.arriving_at and len(self.order_id) > 0:
            print("Drone " + self.name + " is delivering order " + str(self.order_id[0]) + " at " + str(self.arriving_at))
            # print("Drone will be free at " + str(self.free_at))
        else:
            print("Drone " + self.name + " is lost.")
        return orders

    def deliver(self, order, ct=current_time):
        order = orders[order]
        order = order.dropoff(ct)
        self.order_id.pop(0)
        self.location = self.going_to
        if len(self.order_id) > 0:
            via, route_time = march.plan_route(self.location, orders[self.order_id[0]].location, self.speed)
            self.going_to = stores[via] # make this the "via" location
            self.arriving_at = ct + datetime.timedelta(minutes=route_time)
            orders[self.order_id[0]].fulfilled_by = via
            orders[self.order_id[0]].delivered_by = self.name
        else:
            self.going_to = self.home_loc
            self.arriving_at = ct + datetime.timedelta(minutes=c.calc_time(c.calc_distance(self.location, self.going_to), self.speed))
        return order
    
    def assign(self, order, ct=current_time):
        self.order_id.append(order.id)
        via, route_time = march.plan_route(self.location, order.location, self.speed)
        order.assign(self.name, via)
        print("Order assigned to " + self.name + " via " + via + " Num Orders: " + str(len(self.order_id)) + " Route time: " + str(route_time))
        c.print_a_drone(self)
        if len(self.order_id) == 1:
            self.free_at = ct + datetime.timedelta(minutes=route_time)
            self.arriving_at = ct + datetime.timedelta(minutes=route_time)
            self.going_to = stores[via]
        elif len(self.order_id) > 1:
            max_free = max(self.free_at, ct)
            self.free_at = max_free + datetime.timedelta(minutes=route_time)
        c.print_a_drone(self)
        return self, order

    def move(self, adv, ct=current_time):
        moved = adv*self.speed # how many meters the drone can move
        if self.going_to != self.location:
            print("Drone " + self.name + " moved " + str(moved) + " meters.")
            print("Drone " + self.name + " was at " + str(self.location))
            self.location = c.calc_move(self.location, self.going_to, moved)
            print("Drone " + self.name + " moved to " + str(self.location))
        else:
            if len(self.order_id) > 0:
                self.going_to = orders[self.order_id[0]].location
                print("Drone " + self.name + " has picked up their order!")
            elif len(self.order_id) == 0 and self.location != self.home_loc: 
                print("Drone " + self.name + " did not move and is lost!")
            elif len(self.order_id) == 0 and self.location == self.home_loc:
                print("Drone " + self.name + " is home safe!")

class Order:
    def __init__(self, id, address, time):
        self.id = id
        self.ordered_at = time
        self.address = address
        self.location = town[address]
        self.delivered_by = "" # drone from time_marches_on
        self.fulfilled_by = "" # store from time_marches_on
        self.fulfilled_at = "" # populate with current time when fulfilled
    
    def dropoff(self, ct=current_time):
        self.fulfilled_at = ct
        return self

    def assign(self, delivered, fulfilled):
        self.delivered_by = delivered
        self.fulfilled_by = fulfilled
        return

# Read in address files to dictionary

def print_orders(inc_delivered = False):
    print(" ==================================================================")
    print("    Orders:\n")
    for o in orders:
        if inc_delivered:
            c.print_an_order(o)
        else:
            if o.fulfilled_at == "":
                c.print_an_order(o)
    return 

def print_drones():
    print(" ==================================================================")
    print("    Drones:\n")
    for d in drones:
        c.print_a_drone(d)
    return

# Main control loop
print("Beginning cookie delivery service...")
dir_path = os.path.dirname(os.path.realpath(__file__))
stores = c.read_address_file(os.path.join(dir_path, "stores.txt"))
town = c.read_address_file(os.path.join(dir_path, "normal.txt"))
d_names = ["Chipper", "Snicker", "Oatmeal", "Chunk"]
d_speeds = [250, 150, 100, 200]
# intialize the drones:  
for s in stores: 
    print(s)
    drones.append(Drone(d_names[d_id], s))
    drones[d_id].speed = d_speeds[d_id]
    d_id += 1
print("Drones initialized.")
#
# If you would like to play with this, look up "Normal, IL" on google maps and pick out some random addresses to try
# Or try the random feature built in. 
print(" \n\n==================================================================")
print("    Hello! Welcome to the Normal, IL Cookie Delivery Service.")
print("    The Current time is: " + str(current_time))
print("    Please listen carefully as our menu otions have changed.")
print("    Enter a street address to place an order (No city, state, zip).")
print("    Press R for a random address.")
print("    Press Q to quit.")
print("    Press F to fast forward time.")
print("    Press P to print out current environment.")
print("    Press M to print out a map of the current environment.")
print("    Press N to add a new drone.")
print("    Press enter to advance 1 minute by default")
print(" ==================================================================")
while True:
    adv_time = 1
    try:
        print("\n   Current time is: " + str(current_time))
        print("    | (Q)uit | (R)andom | (F)astforward | (P)rint | (N)ew Drone | (M)ap")
        del_addy = input("    | Or Enter Address: ")
        if del_addy == "Q":
            print("Thank you for using the Normal, IL Cookie Delivery Service!")
            print_orders(True)
            print_drones()
            break
        elif del_addy == "R":
            print("Random order placed")
            del_addy = random.choice(list(town.keys()))
            orders.append(Order(id, del_addy, current_time))
            id += 1
        elif del_addy == "F":
            adv_time = input("Enter number of minutes to fast forward: ")
            adv_time = int(adv_time)
        elif del_addy == "P":
            print("    Current time is: " + str(current_time) + "\n")
            print_orders()
            print_drones()
        elif del_addy == "M":
            print("    Printing map....")
            map.plot_map(stores, orders, drones)
        elif del_addy == "":
            pass
        elif del_addy == "T":
            print("Test Functionality")
            print(stores["117 east beaufort street, NORMAL, IL 61761"])
        elif del_addy == "N":
            print("    Adding a new drone!")
            nd_store = input("    What store number is this drone from? (0-3): ")
            nd_name = input("    What is this drone's name? ")
            nd_store = int(nd_store)
            nd_store = list(stores.keys())[nd_store]
            print("Assigning " + str(nd_name) + " to " + str(nd_store))
            drones.append(Drone(nd_name, nd_store))
            nd_speed = input("    How fast is this drone? (~100-400): ")
            nd_speed = int(nd_speed)
            drones[d_id].speed = nd_speed
            d_id += 1
        else:
            del_addy = del_addy.lower()
            del_addy = del_addy + ", normal, IL 61761"
            try:
                loc = town[del_addy]
            except KeyError as k:
                print("Sorry, it seems that address is not in our delivery zone")
                print("Or you selected an invalid menu option: " + str(k))
                print("Please note: Try spelling out the street suffix (e.g. street, avenue, etc.)")
                print("Please try again.")
            orders.append(Order(id, del_addy, current_time))
            id += 1
            pass
    except Exception as e:
        print(traceback.format_exc())
        print_orders(True)
        print_drones()
        continue

    current_time, drones, orders = march.time_marches_on(current_time, adv_time, drones, orders)