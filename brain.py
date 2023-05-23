from random import choice, randrange
import base64
import numpy as np
from nodes import *


class NNet:
    def __init__(self, inputNodes, hiddenLayers, Outputs, genome_size, x, y, cellsLoc):
        self.cellX = x
        self.cellY = y
        self.cellInputs = []
        self.cellsLoc = []
        self.inputsToReturn = []
        self.randomizedEyesightStrength = random()
        for i in range(genome_size-1):
            current_choice = choice(inputNodes)
            try:
                self.currentchoiceis = current_choice(
                    self.randomizedEyesightStrength, x, y, cellsLoc)
                self.degrees = (self.currentchoiceis.strengtha,
                                self.currentchoiceis.strengthb)
            except:
                self.currentchoiceis = current_choice(x, y, cellsLoc)
            self.cellInputs.append(current_choice)

        self.cellHidden = [choice(hiddenLayers)
                           for i in range(genome_size)]
        self.cellOutput = [choice(Outputs)
                           for i in range(genome_size-1)]

    def feedForeward(self):
        genomes = []  # Create a list to store individual cell genomes
        outputs = []  # Store the outputs of each cell

        for i in self.cellInputs:
            # Calculate the input weights for the current cell
            try:
                self.InputWeight = i(self.randomizedEyesightStrength, self.cellX,
                                     self.cellY, self.cellsLoc).activate()
            except:
                self.InputWeight = i(self.cellX, self.cellY,
                                     self.cellsLoc).activate()

            thing = []
            outputss = []

            for hidden in self.cellHidden:
                thing.append(hidden(self.InputWeight).activate())
            for output in self.cellOutput:
                outputss.append(output(sum(thing)).activate())

            # Create a genome list for the current cell
            genome = []
            genome.append(
                base64.b64encode(str(self.InputWeight.tolist()).encode("ascii")).decode("ascii"))
            genome.append([
                base64.b64encode(str(weight.tolist()).encode(
                    "ascii")).decode("ascii")
                for weight in thing
            ])
            genome.append([
                base64.b64encode(str(output.tolist()).encode(
                    "ascii")).decode("ascii")
                for output in outputss
            ])

            # Append the current cell's genome to the genomes list
            genomes.append(genome)

            outputs.append(outputss)  # Store the outputs of each cell

        Genome = " "
        for cell_genome in genomes:
            cell_genome_str = " ".join(["".join(gene) for gene in cell_genome])
            Genome += cell_genome_str + " "

        return self.cellOutput[outputs.index(max(outputs))], Genome

