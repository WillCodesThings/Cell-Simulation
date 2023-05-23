import numpy as np
import math
from random import random
# NODES TO MAKE
# Kill Node (send bacteriophages) (output)
# Is getting killed (input)
# population stimulus (input)
# defend (defense for kill node 50% chance to work.)

# WEIGHTS (LITTERALY NUMBERS) #

# Omnivore/Carnivore (weight on consume node)
# Size (weight on speed)(and energy is higher)
# Speed (weight on move calls per turn)
# energy (for death or not)

# NODES COMPLETED #
# Move Node #
# EYESIGHT #
# TOUCH #

# Get all cell/biomass positions.
# Check for distance between biomass positions and other cells,
# if within view distance then it should calculate a weight
# based on how many objects it sees, Should not compute other cell positions if
# Not a carivore.
# create FOV using positions on canvas for PyGame/A list, (probably will use pygame)


class eyesight:

    def __init__(self, eyesightStrength, x, y, cellsLoc):
        self.value = 0.0
        # in this case strength == theta
        self.biomassLoc = cellsLoc
        self.seenCells = []
        self.strengtha = (90 + (eyesightStrength * 25))
        self.strengthb = (90 - (eyesightStrength * 25))
        self.cellX = x
        self.cellY = y
        self.carnivoreRate = random()
        self.radius = (eyesightStrength*15)
        self.cellsLoc = cellsLoc
        print(self.strengtha)
        print(self.strengthb)

    def rotateL(self):
        self.strengtha += 5
        self.strengthb += 5

    def rotateR(self):
        self.strengtha -= 5
        self.strengthb -= 5

    def activate(self):
        return self.getraycast()

    def getraycast(self):
        # (x,y)=(12∗sin(115),12∗cos(115))
        self.cellview = self.cellY + self.radius

        self.pointa = (self.radius * (math.cos(math.radians(self.strengtha))),
                       (self.radius * math.sin(math.radians(self.strengtha))))
        self.pointb = ((math.cos(math.radians(self.strengthb))),
                       (self.radius * math.sin(math.radians(self.strengthb))))

        print(round((self.pointa[0]), 2), round(self.pointa[1], 2))
        print(round(self.pointb[0], 2), round(self.pointb[1], 2))
        print(self.cellX)
        print(self.cellY)
        # self.cellsLoc = [[0,0], [3,3], [10,7]]

        # fixed Inverse Tan function, was producing wrong result.
        # Had to use inverse tan squared.
        # Just subtracts the first cell Y by the current cell Y and passes that in,
        # then it passes in the first cell X subtracted by the current cellX
        # Need to pass in like math.atan2((y2 - y1), (x2-x1))
        # then convert from radians to degrees.

        for i in self.cellsLoc:
            self.Cellangle = math.degrees(math.atan2(
                (i[1] - self.cellY), (i[0] - self.cellX)))
            print("CURRENT CELL EVALUTATION")
            print(i)
            print("CELL ANGLE")
            print(self.Cellangle)
            print("STRENGTHS")
            print(self.strengtha, self.strengthb)
            print("RADIUS")
            print(self.radius)
            print("\n\n")
            if (((self.Cellangle <= self.strengtha) and (self.Cellangle >= self.strengthb))):
                if (math.sqrt((i[0]-self.cellX)**2 + (i[1]-self.cellY)**2) <= self.radius):
                    self.seenCells.append(i)

        return self.sigmoid(len(self.seenCells))

    def sigmoid(self, x):
        # Sigmoid activation function
        return 1 / (1 + np.exp(-x))


class Touch:
    def __init__(self, x, y, cellsLoc):
        self.cellX = x
        self.cellY = y
        self.cellsLoc = cellsLoc
        self.TouchingCells = []

    def sigmoid(self, x):
        # Sigmoid activation function
        return 1 / (1 + np.exp(-x))

    def activate(self):
        return self.sigmoid(self.getinput())

    def getinput(self):
        for i in self.cellsLoc:
            if ((i[0] >= (self.cellX-1)) and (i[0] <= (self.cellX+1))) and ((i[1] >= (self.cellY-1)) and ((i[1] <= self.cellY + 1))):
                self.TouchingCells.append((self.cellX, self.cellY))
        return len(self.TouchingCells)


class Consume:
    def __init__(self, inputWeight):
        self.inputweight = inputWeight
        self.randomMultiplier = random()
        self.randomAdder = random()

    def activate(self):
        return self.sigmoid(self.inputweight * self.randomMultiplier)

    def sigmoid(self, x):
        # Sigmoid activation function
        return 1 / (1 + np.exp(-x))


class RotationR:
    def __init__(self, incoming_weights):
        self.weight = random()
        self.incoming_weights = incoming_weights * self.weight

    def activate(self):
        return self.incoming_weights


class RotationL:
    def __init__(self, incoming_weights, ):
        self.weight = random()
        self.incoming_weights = incoming_weights * self.weight

    def activate(self):
        return self.incoming_weights


class MoveF:
    def __init__(self, incoming_weight):
        self.incoming_weight = incoming_weight
        self.weight = random()

    def sigmoid(self, x):
        # Sigmoid activation function
        return 1 / (1 + np.exp(-x))

    def activate(self):
        return self.sigmoid((self.incoming_weight * self.weight))


class MoveB:
    def __init__(self, incoming_weight):
        self.incoming_weight = incoming_weight
        self.weight = random()

    def sigmoid(self, x):
        # Sigmoid activation function
        return 1 / (1 + np.exp(-x))

    def activate(self):
        return self.sigmoid((self.incoming_weight * self.weight))


class MoveR:
    def __init__(self, incoming_weight):
        self.incoming_weight = incoming_weight
        self.weight = random()

    def sigmoid(self, x):
        # Sigmoid activation function
        return 1 / (1 + np.exp(-x))

    def activate(self):
        return self.sigmoid((self.incoming_weight * self.weight))


class MoveL:
    def __init__(self, incoming_weight):
        self.incoming_weight = incoming_weight
        self.weight = random()

    def sigmoid(self, x):
        # Sigmoid activation function
        return 1 / (1 + np.exp(-x))

    def activate(self):
        return self.sigmoid((self.incoming_weight * self.weight))


class HiddenNode:

    def __init__(self, incoming_connections):
        self.value = 0.0
        self.incoming_connections = incoming_connections
        self.weight = random()

    def activate(self):
        # Apply the activation function to calculate the node's output value
        # Here, we assume a simple activation function such as the sigmoid function
        return self.sigmoid(self.get_input_sum())

    def get_input_sum(self):
        # Calculate the sum of the inputs from the incoming connections
        input_sum = 0.0
        print(self.incoming_connections)
        print(self.weight)
        input_sum += self.incoming_connections * self.weight
        return input_sum

    def sigmoid(self, x):
        # Sigmoid activation function
        return 1 / (1 + np.exp(-x))


class OutputNode:

    def __init__(self, incoming_connections):
        self.value = 0.0
        self.incoming_connections = incoming_connections

    def activate(self):
        # Apply the activation function to calculate the node's output value
        # Here, we assume a simple activation function such as the sigmoid function
        self.value = self.sigmoid(self.get_input_sum())

    def get_input_sum(self):
        # Calculate the sum of the inputs from the incoming connections
        input_sum = 0.0
        for connection in self.incoming_connections:
            input_sum += connection.weight * connection.in_node.value
        return input_sum

    def sigmoid(self, x):
        # Sigmoid activation function
        return 1 / (1 + np.exp(-x))
