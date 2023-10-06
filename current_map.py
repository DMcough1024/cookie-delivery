import matplotlib.pyplot as plt
import numpy as np
img = plt.imread('normal_map2.png')

# Create a map using matplotlib of the current locations of everyone
def plot_map(stores, orders, drones):
    store_x = []
    store_y = []
    order_x = []
    order_y = []
    drone_x = []
    drone_y = []
    going_x = []
    going_y = []

    for s in stores:
        x = float(stores[s].split(',')[0])
        y = float(stores[s].split(',')[1])
        store_x.append(x)
        store_y.append(y)
    for o in orders:
        x = float(o.location.split(',')[0])
        y = float(o.location.split(',')[1])
        order_x.append(x)
        order_y.append(y)
    for d in drones:
        x = float(d.location.split(',')[0])
        y = float(d.location.split(',')[1])
        drone_x.append(x)
        drone_y.append(y)
        x = float(d.going_to.split(',')[0])
        y = float(d.going_to.split(',')[1])
        going_x.append(x)
        going_y.append(y)

    fig, ax = plt.subplots()
    ax.imshow(img, extent=[-89.069454, -88.902522, 40.488157, 40.564864])
    plt.scatter(store_x, store_y, color='red', label='Stores', marker='*', alpha=0.5, s=200)
    plt.scatter(order_x, order_y, color='blue', label='Orders', s=20)
    plt.scatter(drone_x, drone_y, color='green', label='Drones', marker='d', s=75)
    plt.scatter(going_x, going_y, color='orange', label='Going To', s=20)
    plt.legend()
    plt.show()
    
    return
    
