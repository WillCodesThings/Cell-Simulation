from random import choice, randrange
import base64
import numpy as np
from nodes import *

# weights example

# weights = {
#  'BaseSpeed' : 0.2
#  'BaseSight' : 0.1
#  'BaseSensory' : 0.1
# }


class NNet:
    def __init__(self, inputNodes, hiddenLayers, Outputs, genome_size, x, y, cellsLoc):
        self.cellX = x
        self.timesRun = 0
        self.cellY = y
        self.hiddenWeights = []
        self.outputWeights = []
        self.cellInputs = []
        self.cellsLoc = []
        self.inputsToReturn = []
        self.randomizedEyesightStrength = random()
        self.carnivoreRate = random()
        self.genome_size = genome_size
        self.INPUTNODES = inputNodes
        self.HIDDENNODES = hiddenLayers
        self.OUTPUTNODES = Outputs
        for i in range(genome_size - 2):
            current_choice = choice(inputNodes)
            try:
                self.currentchoiceis = current_choice(
                    self.randomizedEyesightStrength, x, y, cellsLoc
                )
                self.degrees = (
                    self.currentchoiceis.strengtha,
                    self.currentchoiceis.strengthb,
                )
            except:
                self.currentchoiceis = current_choice(x, y, cellsLoc)
            self.cellInputs.append(current_choice)

        self.cellHidden = [choice(hiddenLayers) for i in range(genome_size)]
        self.cellOutput = [choice(Outputs) for i in range(genome_size - 1)]

    def mutate(self, mutationRate):
        self.mutate = mutationRate
        if random() >= 0.6:
            self.mutate = -mutationRate
        self.randomizedEyesightStrength += mutationRate
        for hidden in self.hiddenWeights:
            if random() >= 0.6:
                self.mutate = -mutationRate
            else:
                self.mutate = mutationRate
            hidden += mutationRate
        for output in self.outputWeights:
            if random() >= 0.6:
                self.mutate = -mutationRate
            else:
                self.mutate = mutationRate
            output += mutationRate
        if random() <= mutationRate:
            self.rerollNodes()

    def rerollNodes(self):
        randomChoice = randrange(1, 2)
        if randomChoice == 1:
            for i in range(self.genome_size - 2):
                current_choice = choice(self.INPUTNODES)
                try:
                    self.currentchoiceis = current_choice(
                        self.randomizedEyesightStrength,
                        self.cellX,
                        self.cellY,
                        self.cellsLoc,
                    )
                    self.degrees = (
                        self.currentchoiceis.strengtha,
                        self.currentchoiceis.strengthb,
                    )
                except:
                    self.currentchoiceis = current_choice(
                        self.cellX, self.cellY, self.cellsLoc
                    )
                self.cellInputs.append(current_choice)
        elif randomChoice == 2:
            self.cellOutput = [choice(self.OUTPUTNODES) for i in range(genome_size - 1)]

    def feedForeward(self):
        genomes = []  # Create a list to store individual cell genomes
        outputs = []  # Store the outputs of each cell

        for i in self.cellInputs:
            # Calculate the input weights for the current cell
            try:
                self.InputWeight = i(
                    self.randomizedEyesightStrength,
                    self.cellX,
                    self.cellY,
                    self.cellsLoc,
                )
            except:
                self.InputWeight = i(self.cellX, self.cellY, self.cellsLoc)

            thing = []
            outputss = []
            if self.timesRun >= 1:
                for hidden in self.cellHidden:
                    thing.append(
                        hidden(
                            self.InputWeight.activate(),
                            self.hiddenWeights[self.cellHidden.index(hidden)],
                        ).activate()
                    )
                for output in self.cellOutput:
                    outputss.append(
                        output(
                            sum(thing),
                            self.outputWeights[self.cellOutput.index(output)],
                        ).activate()
                    )
            else:
                for hidden in self.cellHidden:
                    # need to save weights, otherwise are always randomized when activating nodes.
                    hiddenthing = hidden(self.InputWeight.activate(), None)
                    self.hiddenWeights.append(hiddenthing.weight)
                    thing.append(hiddenthing.activate())
                for output in self.cellOutput:
                    currentOuput = output(sum(thing), None)
                    self.outputWeights.append(currentOuput.weight)
                    outputss.append(currentOuput.activate())

            # Create a genome list for the current cell
            genome = []
            genome.append(
                base64.b64encode(
                    str(self.InputWeight.activate().tolist()).encode("ascii")
                ).decode("ascii")
            )
            genome.append(
                [
                    base64.b64encode(str(weight.tolist()).encode("ascii")).decode(
                        "ascii"
                    )
                    for weight in thing
                ]
            )
            genome.append(
                [
                    base64.b64encode(str(output.tolist()).encode("ascii")).decode(
                        "ascii"
                    )
                    for output in outputss
                ]
            )

            # Append the current cell's genome to the genomes list
            genomes.append(genome)

            outputs.append(outputss)  # Store the outputs of each cell
        Genome = " "
        for cell_genome in genomes:
            cell_genome_str = " ".join(["".join(gene) for gene in cell_genome])
            Genome += cell_genome_str + " "
        self.timesRun += 1

        FINALOUTPUT = self.cellOutput[outputs.index(max(outputs))](1, 1)
        outputs = []
        return FINALOUTPUT, Genome
