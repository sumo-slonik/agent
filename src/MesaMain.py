import matplotlib.pyplot as plt
import mesa

from DnaClasses import Agent


def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "Color": "red",
        "r": 0.5,
    }
    return portrayal


class Model(mesa.Model):

    def __init__(self, N, width=10,height=10):
        self.num_agents = N
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, True)
        # Create agents
        for i in range(self.num_agents):
            a = Agent(10, i, self)
            self.schedule.add(a)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()

    def add_agent(self, agent):
        self.schedule.add(agent)
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        self.grid.place_agent(agent, (x, y))
        self.num_agents += 1


if __name__ == '__main__':
    model = Model(10)
    model.step()

    tTolerance = [a.DNA.returnAgentStructure().tTolerance for a in model.schedule.agents]
    plt.hist(tTolerance, label="tTolerance")
    plt.xlabel("tTolerance value")
    plt.ylabel("agents number")
    plt.show()

    tTolerance = [a.DNA.returnAgentStructure().hTolerance for a in model.schedule.agents]
    plt.hist(tTolerance, label="hTolerance")
    plt.xlabel("hTolerance value")
    plt.ylabel("agents number")
    plt.show()

    tTolerance = [a.DNA.returnAgentStructure().wTolerance for a in model.schedule.agents]
    plt.hist(tTolerance, label="wTolerance")
    plt.xlabel("wTolerance value")
    plt.ylabel("agents number")
    plt.show()

    tTolerance = [a.DNA.returnAgentStructure().maxVelocity for a in model.schedule.agents]
    plt.hist(tTolerance, label="maxVelocity")
    plt.xlabel("maxVelocity value")
    plt.ylabel("agents number")
    plt.show()

    tTolerance = [a.DNA.returnAgentStructure().maxEnergy for a in model.schedule.agents]
    plt.hist(tTolerance, label="maxEnergy")
    plt.xlabel("maxEnergy value")
    plt.ylabel("agents number")
    plt.show()

    tTolerance = [a.DNA.returnAgentStructure().maxView for a in model.schedule.agents]
    plt.hist(tTolerance, label="maxView")
    plt.xlabel("maxView value")
    plt.ylabel("agents number")
    plt.show()

    tTolerance = [a.DNA.returnAgentStructure().maxAcceleration for a in model.schedule.agents]
    plt.hist(tTolerance, label="maxAcceleration")
    plt.xlabel("maxAcceleration value")
    plt.ylabel("agents number")
    plt.show()

    tTolerance = [a.DNA.returnAgentStructure().feroReaction for a in model.schedule.agents]
    plt.hist(tTolerance, label="feroReaction")
    plt.xlabel("feroReaction value")
    plt.ylabel("agents number")
    plt.show()
    grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)
    server = mesa.visualization.ModularServer(
        Model, [grid], "Evolution simulation", {"N": 5, "width": 10, "height": 10}
    )
    server.port = 8080  # The default
    server.launch()
