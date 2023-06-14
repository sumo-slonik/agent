import random
from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def movie(self, x, y):
        pass


class RandomWalker(Strategy):

    def movie(self, x, y):
        x += random.randint(-5, 5)
        y += random.randint(-5, 5)
        return (x, y)


class BiomChanger(Strategy):
    actualDirectory = 0
    firstTime = True

    def movie(self, x, y):
        if self.firstTime:
            self.actualDirectory = random.randint(0, 4)
            self.firstTime = False
        else:
            if self.actualDirectory == 0:
                x += 1
            elif self.actualDirectory == 1:
                x -= 1
            elif self.actualDirectory == 2:
                y += 1
            elif self.actualDirectory == 3:
                y -= 1
        return (x, y)
