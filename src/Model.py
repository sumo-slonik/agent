import random

import mesa

from Dna import CompanyStructure, StructureDelta, DNA
from src.Strategy import RandomWalker, BiomChanger


def agent_portrayal(agent):
    if type(agent) is Food:
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Layer": 0,
            "Color": "green",
            "r": 1.2,
        }
    else:
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Layer": 0,
            "Color": "red",
            "r": 0.5,
        }
        if type(agent.strategy) is BiomChanger:
            portrayal["Color"] = "purple"
    return portrayal


class Food(mesa.Agent):
    def __init__(self, unique_id, model: mesa.Model, enegry):
        super().__init__(unique_id, model)
        self.energy = enegry

    def remove_agent(self):
        self.model.num_agents -= 1
        self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)


class Agent(mesa.Agent):
    def __init__(self, unique_id, model: mesa.Model, structure_delta=None,
                 dna_len=5):
        super().__init__(unique_id, model)
        self.structure_delta = structure_delta
        self.energy = random.randint(50, 100)
        self.dna = DNA(dna_len, structure_delta=structure_delta)
        self.sleepMult = 0
        self.strategy = RandomWalker() if (random.randint(0, 2) % 2 == 0) else BiomChanger()

    def step(self):
        if self.energy == 0:
            self.remove_agent()
        if self.pos is not None:
            self.energy -= 1
            print(self.energy, self.unique_id)
            if self.sleepMult > 0:
                self.sleepMult -= 1
            canMultipleWith: [Agent] = self.model.grid.get_cell_list_contents([self.pos])
            if canMultipleWith:
                canMultipleWith = list(filter(lambda x: type(x) is not Food and x.sleepMult == 0, canMultipleWith))
                canMultipleWith.sort(key=lambda x: x.energy, reverse=True)
                first = None
                second = None
                if len(canMultipleWith) > 2:
                    first = canMultipleWith[0]
                    second = canMultipleWith[1]
            if first and second:
                dna: DNA = first.dna * second.dna
                print("nowe dna")
                print(dna.returnDeltaStructure())
                child = Agent(self.model.num_agents + random.randint(1e12, 1e13), self.model,
                              dna.returnDeltaStructure(),
                              dna.dnaLength)
                self.model.add_agent(child)
                pass
                # child = first * second
                # self.model.add_agent(child)
            food: [Food] = filter(lambda x: type(x) == Food, self.model.grid.get_cell_list_contents([self.pos]))
            for i in food:
                self.energy += i.energy
                i.remove_agent()
            x, y = self.strategy.movie(self.pos[0], self.pos[1])
            self.model.grid.move_agent(self, (x, y))
            # direction = random.randint(0, 5)
            #
            # if direction == 0:
            #     self.model.grid.move_agent(self, (self.pos[0] + 1, self.pos[1]))
            # if direction == 1:
            #     self.model.grid.move_agent(self, (self.pos[0], self.pos[1] + 1))
            # if direction == 2:
            #     self.model.grid.move_agent(self, (self.pos[0] - 1, self.pos[1]))
            # if direction == 3:
            #     self.model.grid.move_agent(self, (self.pos[0], self.pos[1] - 1))

    def remove_agent(self):
        self.model.num_agents -= 1
        self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)


class Model(mesa.Model):
    def __init__(self, N, width=10,
                 height=10):
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.num_agents = N
        self.schedule = mesa.time.RandomActivation(self)
        for i in range(self.num_agents):
            random_numbers = [round(random.uniform(-2, 2), 2) for _ in range(5)]
            delta = StructureDelta(random_numbers[0],
                                   random_numbers[1],
                                   random_numbers[2],
                                   random_numbers[3],
                                   random_numbers[4])
            a = Agent(i, self, structure_delta=delta)
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
        for i in range(int(self.grid.width / 5)):
            a = Food(random.randint(1e12, 1e13), self, random.randint(0, 100))
            self.schedule.add(a)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        if self.num_agents > 0:
            self.schedule.step()

    def add_agent(self, agent):
        agent.structure_delta.visualize(str(self.schedule.steps))
        print("poród")
        print(self.schedule.steps)
        print(agent.energy)

        self.schedule.add(agent)
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        self.grid.place_agent(agent, (x, y))
        self.num_agents += 1


if __name__ == '__main__':
    grid = mesa.visualization.CanvasGrid(agent_portrayal, 100, 100, 500, 500)
    server = mesa.visualization.ModularServer(
        Model, [grid], "Evolution simulation",
        {"N": 80, "width": 100, "height": 100}
    )
    server.port = 8521  # The default
    server.launch()
