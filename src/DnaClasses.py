import random

import mesa

NUMBER_OF_ELEMENTS = 12


class AgentStructure:
    tTolerance = 0
    hTolerance = 0
    wTolerance = 0
    maxVelocity = 0
    maxEnergy = 0
    maxAcceleration = 0
    maxView = 0
    feroReaction = 0
    feroGround = 0
    feroAgent = 0
    energyPerTime = 0
    controlSum = 0

    def __init__(self, tTolerance, hTolerance, wTolerance, maxVelocity, maxEnergy, maxAcceleration, maxView
                 , feroReaction, feroGround, feroAgent, energyPerTime, controlSum):
        self.tTolerance = tTolerance
        self.hTolerance = hTolerance
        self.wTolerance = wTolerance
        self.maxVelocity = maxVelocity
        self.maxEnergy = maxEnergy
        self.maxView = maxView
        self.maxAcceleration = maxAcceleration
        self.feroReaction = feroReaction
        self.feroGround = feroGround
        self.feroAgent = feroAgent
        self.energyPerTime = energyPerTime
        self.controlSum = controlSum

    def __str__(self) -> str:
        return "tTolerance " + str(self.tTolerance) + "\n" + \
            "hTolerance " + str(self.hTolerance) + "\n" + \
            "wTolerance " + str(self.wTolerance) + "\n" + \
            "maxVelocity " + str(self.maxVelocity) + "\n" + \
            "maxEnergy " + str(self.maxEnergy) + "\n" + \
            "maxView " + str(self.maxView) + "\n" + \
            "maxAcceleration " + str(self.maxAcceleration) + "\n" + \
            "feroReaction " + str(self.feroReaction) + "\n" + \
            "feroGround " + str(self.feroGround) + "\n" + \
            "feroAgent " + str(self.feroAgent) + "\n" + \
            "energyPerTime " + str(self.energyPerTime) + "\n" + \
            "controlSum " + str(self.controlSum)


class DNA:
    dnaLength = 0
    dnaCode = []

    def __init__(self, dnaLength: int, dnaCode=[]):
        self.dnaLength = dnaLength
        self.dnaCode = dnaCode if dnaCode else [random.uniform(0, 1 / dnaLength) for _ in
                                                range(dnaLength * NUMBER_OF_ELEMENTS)]

    def returnAgentStructure(self):
        tTolerance = 0
        hTolerance = 0
        wTolerance = 0
        maxVelocity = 0
        maxEnergy = 0
        maxAcceleration = 0
        maxView = 0
        feroReaction = 0
        feroGround = 0
        feroAgent = 0
        energyPerTime = 0
        controlSum = 0
        for index, value in enumerate(self.dnaCode):
            if index % 12 == 0:
                tTolerance += value
            elif index % 12 == 1:
                hTolerance += value
            elif index % 12 == 2:
                wTolerance += value
            elif index % 12 == 3:
                maxVelocity += value
            elif index % 12 == 4:
                maxEnergy += value
            elif index % 12 == 5:
                maxAcceleration += value
            elif index % 12 == 6:
                maxView += value
            elif index % 12 == 7:
                feroReaction += value
            elif index % 12 == 8:
                feroGround += value
            elif index % 12 == 9:
                feroAgent += value
            elif index % 12 == 10:
                energyPerTime += value
            elif index % 12 == 11:
                controlSum += value

        return AgentStructure(tTolerance,
                              hTolerance,
                              wTolerance,
                              maxVelocity,
                              maxEnergy,
                              maxAcceleration,
                              maxView,
                              feroReaction,
                              feroGround,
                              feroAgent,
                              energyPerTime, 1)


class Agent(mesa.Agent):
    DNA = None
    # multiplication offset
    sleepMult = 0
    energy = 0
    AgentStructure = None

    def __init__(self, dnaLength, unique_id, model, dna=[]):
        super().__init__(unique_id, model)
        self.wealth = 1
        if dna:
            self.DNA = dna
        else:
            self.DNA = DNA(dnaLength, [])
        self.AgentStructure = AgentStructure(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.energy = self.AgentStructure.maxEnergy

    def step(self):
        # The agent's step will go here.
        # For demonstration purposes we will print the agent's unique_id
        # print("Hi, I am agent " + str(self.unique_id) + " " + str(self.DNA.returnAgentStructure()))
        print("My position " + str(self.pos))
        print("neighbours " + str(self.model.grid.get_cell_list_contents([self.pos])))
        canMultipleWith: [Agent] = self.model.grid.get_cell_list_contents([self.pos])
        if self.sleepMult > 0:
            self.sleepMult -= 1
        canMultipleWith = list(filter(lambda x: x.sleepMult == 0, canMultipleWith))
        canMultipleWith.sort(key=lambda x: x.energy, reverse=True)
        first = None
        second = None
        if len(canMultipleWith) > 2:
            first = canMultipleWith[0]
            second = canMultipleWith[1]
        direction = random.randint(0, 5)
        if first and second:
            child = first * second
            self.model.add_agent(child)

        if direction == 0:
            self.model.grid.move_agent(self, (self.pos[0] + 1, self.pos[1]))
        if direction == 1:
            self.model.grid.move_agent(self, (self.pos[0], self.pos[1] + 1))
        if direction == 2:
            self.model.grid.move_agent(self, (self.pos[0] - 1, self.pos[1]))
        if direction == 3:
            self.model.grid.move_agent(self, (self.pos[0], self.pos[1] - 1))

    def __mul__(self, other):
        if type(other) is not Agent:
            return
        firstDNA = self.DNA.dnaCode
        secondDNA = other.DNA.dnaCode
        minLength = min(len(firstDNA), len(secondDNA))
        crossPoint = random.randint(0, minLength) % NUMBER_OF_ELEMENTS
        resultDna = firstDNA if len(firstDNA) > len(secondDNA) else secondDNA
        resultDna = resultDna[:-crossPoint] + (firstDNA if len(firstDNA) < len(secondDNA) else secondDNA)[:crossPoint]
        resultDNA = DNA(len(resultDna), resultDna)
        self.sleepMult = 5
        return Agent(len(resultDna), random.random(), self.model, resultDNA)
