import math
import numpy as np
import matplotlib.pyplot as plt

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

# Create Train
emptyTrain = Train()
oil = emptyTrain.addLokomotive('BR 75')
oil = oil.addWagon('Tank Car EU 120', 9)
ice = Train()
ice = ice.addMultiUnit('ICE 1')
train = oil