import mesa
from DnaClasses import Agent
import matplotlib.pyplot as plt


class Model(mesa.Model):


    def __init__(self, N):
        self.num_agents = N
        self.schedule = mesa.time.RandomActivation(self)
        # Create agents
        for i in range(self.num_agents):
            a = Agent(10,i, self)
            self.schedule.add(a)

    def step(self):
        """Advance the model by one step."""
        self.schedule.step()


if __name__ == '__main__':
    model = Model(10)
    model.step()

    tTolerance = [a.DNA.returnAgentStructure().tTolerance for a in model.schedule.agents]
    plt.hist(tTolerance,label="tTolerance")
    plt.xlabel("tTolerance value")
    plt.ylabel("agents number")
    plt.show()

    tTolerance = [a.DNA.returnAgentStructure().hTolerance for a in model.schedule.agents]
    plt.hist(tTolerance,label="hTolerance")
    plt.xlabel("hTolerance value")
    plt.ylabel("agents number")
    plt.show()

    tTolerance = [a.DNA.returnAgentStructure().wTolerance for a in model.schedule.agents]
    plt.hist(tTolerance,label="wTolerance")
    plt.xlabel("wTolerance value")
    plt.ylabel("agents number")
    plt.show()

    tTolerance = [a.DNA.returnAgentStructure().maxVelocity for a in model.schedule.agents]
    plt.hist(tTolerance,label="maxVelocity")
    plt.xlabel("maxVelocity value")
    plt.ylabel("agents number")
    plt.show()

    tTolerance = [a.DNA.returnAgentStructure().maxEnergy for a in model.schedule.agents]
    plt.hist(tTolerance,label="maxEnergy")
    plt.xlabel("maxEnergy value")
    plt.ylabel("agents number")
    plt.show()

    tTolerance = [a.DNA.returnAgentStructure().maxView for a in model.schedule.agents]
    plt.hist(tTolerance,label="maxView")
    plt.xlabel("maxView value")
    plt.ylabel("agents number")
    plt.show()

    tTolerance = [a.DNA.returnAgentStructure().maxAcceleration for a in model.schedule.agents]
    plt.hist(tTolerance,label="maxAcceleration")
    plt.xlabel("maxAcceleration value")
    plt.ylabel("agents number")
    plt.show()

    tTolerance = [a.DNA.returnAgentStructure().feroReaction for a in model.schedule.agents]
    plt.hist(tTolerance,label="feroReaction")
    plt.xlabel("feroReaction value")
    plt.ylabel("agents number")
    plt.show()
