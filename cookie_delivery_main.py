# This program will manage the cookie delivery drones for a fictional city.

# Import the necessary modules 
import os
import random
import datetime 
import math
import order_route as route
import time_marches_on as march
import calculator as c

# Global variables
global id
global current_time
id = 1
current_time = datetime.datetime.now()
current_time = current_time.replace(second=0, microsecond=0)
orders = []
drones = []

# Define classes
class Drone:
    def __init__(self, name, store):
        self.name = name
        self.home = store
        self.going_to = ""
        self.order_id = ""
        self.location = stores[store]
        self.speed = 500 # meters per minute

class Order:
    def __init__(self, id, address, time):
        self.id = id
        self.address = address
        self.location = town[address]
        self.store = route.assign_drone(self, drones).name
        self.ordered_at = time
        self.fulfilled_at = "" # populate with current time when fulfilled
        self.delivered_by = "" # populate with drone name when fulfilled

# Read in address files to dictionary
def read_address_file(filename):
    with open(filename, 'r') as file:
        addy = {}
        for line in file:
            key, value = line.strip().split(':')
            addy[key] = value
    return addy

def print_orders(inc_delivered = False):
    print(" ==================================================================")
    print("    Orders:")
    for o in orders:
        if inc_delivered:
            print(str(o.id) + ": " + o.address + " | " + str(o.ordered_at))
            print("Fulfilled by: " + str(o.store) + "\n")
        else:
            if o.fulfilled_at == "":
                print(str(o.id) + ": " + o.address + " | " + str(o.ordered_at))
                print("Fulfilled by: " + str(o.store) + "\n")
    return 

def print_drones():
    print(" ==================================================================")
    print("    Drones:")
    for d in drones:
        print(d.name + " is heading towards " + d.going_to + " with order " + str(d.order_id))
        print("Current location: " + str(d.location) + "\n")
    return

# Main control loop
print("Beginning cookie delivery service...")
dir_path = os.path.dirname(os.path.realpath(__file__))
stores = read_address_file(os.path.join(dir_path, "stores.txt"))
town = read_address_file(os.path.join(dir_path, "normal.txt"))
# obstacles = read_address_file(os.path.join(dir_path, "obstacles.txt"))
# intialize the drones: 
d = 1 
for s in stores: 
    dn = "Drone " + str(d)
    drones.append(Drone(dn, s))
    d += 1
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
print(" ==================================================================")
while True:
    adv_time = 1
    try:
        print("   Current time is: " + str(current_time) + "\n")
        del_addy = input("   (Q)uit | (R)andom | (F)astforward | (P)rint | Or Enter Address: ")
        if del_addy == "Q":
            print("Thank you for using the Normal, IL Cookie Delivery Service!")
            print_orders(True)
            print_drones()
            break
        elif del_addy == "R":
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
        elif del_addy == "T":
            print(    "Secret test funciton")
            p1 = random.choice(list(town.keys()))
            p2 = random.choice(list(town.keys()))
            print("Distance from: " + p1 + " to " + p2 + " is:")
            print(str(c.calc_distance(town[p1], town[p2])) + " meters")
            print("Time to travel that distance is:")
            print(str(c.calc_time(c.calc_distance(town[p1], town[p2]), 500)) + " minutes")
        else:
            del_addy = del_addy.lower()
            del_addy = del_addy + ", normal, IL 61761"
            orders.append(Order(id, del_addy, current_time))
            id += 1
            pass
    except Exception as e:
        print("Sorry, it seems that address is not in our delivery zone")
        print("Or you selected an invalid menu option: " + str(e))
        print("Please note: Try spelling out the street suffix (e.g. street, avenue, etc.)")
        print("Please try again.")
        continue
    
    current_time = march.time_marches_on(current_time, adv_time)