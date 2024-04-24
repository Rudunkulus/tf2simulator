import math
import numpy as np
import matplotlib.pyplot as plt

# class Lokomotive:
#     def __init__(self):
#         self.topspeed = 0 # [m/s]
#         self.power = 0 # [W]
#         self.traction  = 0 # [N]
#         self.weight = 0 # [kg]
#         self.length = 0 # [m]
#         self.cost = 0 # [$/year]

# class Wagon:
#     def __init__(self):
#         self.topspeed # [m/s]
#         self.weight # [kg]
#         self.length # [m]
#         self.cost # [$/year]
#         self.capacity # [-]

class Train:
    def __init__(self):
        self.topspeed = 300. # [m/s]
        self.power = 0 # [W]
        self.traction = 0 # [N]
        self.weight = 0 # [kg]
        self.length = 0. # [m]
        self.runningCost = 0 # [$/year]
        self.capacity = 0 # [-]

    def addLokomotive(self, name, amount=1):
        for i in range(amount):
            match name:
                case "Series 1042":
                    runningCost = 2111949
                    topspeed = 140.
                    power = 3300
                    traction = 260
                    weight = 84
                    length = 16.2
                case "BR 75":
                    runningCost = 355224
                    topspeed = 90.
                    power = 580
                    traction = 85
                    weight = 76
                    length = 12.6
            self.runningCost += runningCost
            self.power += power * 1000
            self.traction += traction * 1000
            self.weight += weight * 1000
            self.length += length
            self.topspeed = min(self.topspeed, topspeed/3.6)
        return self
    
    def addMultiUnit(self, name, amount=1):
        for i in range(amount):
            match name:
                case "ICE 1":
                    runningCost = 11523056
                    topspeed = 280.
                    power = 8800
                    traction = 200
                    weight = 455
                    length = 282
                    capacity = 162
            self.runningCost += runningCost
            self.power += power * 1000
            self.traction += traction * 1000
            self.weight += weight * 1000
            self.length += length
            self.capacity += capacity
            self.topspeed = min(self.topspeed, topspeed/3.6)
        return self

    def addWagon(self, name, amount):
        for i in range (amount):
            match name:
                case "Tank Car EU 120":
                    runningCost = 180937
                    topspeed = 120.
                    capacity = 15
                    weight = 15
                    length = 11.37
            self.runningCost += runningCost
            self.weight += weight * 1000
            self.length += length
            self.topspeed = min(self.topspeed, topspeed/3.6)
            self.capacity += capacity
        return self

### Soft Parameters

slope = 40 / 1000 # [-]

# Create Train
emptyTrain = Train()
oil = emptyTrain.addLokomotive('BR 75')
oil = oil.addWagon('Tank Car EU 120', 1)
ice = Train()
ice = ice.addMultiUnit('ICE 1')
train = oil

### Hard Parameters
R = 0.00 # roll impact
L = 0. # linear impact
A = 0. # aero impact
P = 0.9 # power scaler
T = 2. # traction scaler
g = 9.81

### Simulation
t = 0.
s = 0.
v = 0.
a = 0.
dt = 0.1

while v < train.topspeed and t < 3600:
    # rolling force
    F_R = -R * train.weight * g

    # linear force
    F_L = -L * v

    # aero force
    F_A = -A * v * v

    # slope force
    alpha = math.atan(slope)
    F_G = - math.sin(alpha) * train.weight * g

    # engine force realistic
    F_E = min(P * train.power / max(v,0.1), train.traction)

    # engine force ingame
    if P * train.power / max(v,0.1) > train.traction:
        F_E *= T

    F_tot = F_E + F_G + F_R + F_L + F_A
    a = F_tot/train.weight
    v += a*dt
    s += v*dt
    t += dt
    # print(t,s,v,a)

if t < 150:
    print('Accelerated to', round(v*3.6), 'km/h in', round(t), 's and', round(s), 'm.')
else:
    print('Accelerated to', round(v*3.6), 'km/h in', round(t/60), 'min and', round(s), 'm.')