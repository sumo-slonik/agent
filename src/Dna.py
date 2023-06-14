import random

import matplotlib.pyplot as plt
import pandas as pd


class StructureDelta:
    nonCurrentAssets = 0
    currentAssets = 0
    equityShareholdersOfTheParent = 0
    nonCurrentLiabilities = 0
    currentLiabilities = 0

    def __init__(self, nonCurrentAssets, currentAssets, equityShareholdersOfTheParent,
                 nonCurrentLiabilities, currentLiabilities):
        self.nonCurrentAssets = nonCurrentAssets
        self.currentAssets = currentAssets
        self.equityShareholdersOfTheParent = equityShareholdersOfTheParent
        self.nonCurrentLiabilities = nonCurrentLiabilities
        self.currentLiabilities = currentLiabilities

    def visualize(self, generacja=0):
        # Dane do wykresu
        values = [self.nonCurrentAssets, self.currentAssets, self.equityShareholdersOfTheParent,
                  self.nonCurrentLiabilities, self.currentLiabilities]
        print("_______________________________")
        print(values)
        print("_______________________________")

        labels = [
            'Aktywa trwałe',
            'Aktywa obrotowe',
            'Kapitał własny udziałowców podmiotu dominującego',
            'Zobowiązania długoterminowe',
            'Zobowiązania krótkoterminowe'
        ]

        # Ustawienia wykresu
        fig, ax = plt.subplots()
        ax.bar(range(len(values)), values, color='blue')

        # Ustawienia osi X
        ax.set_xticks(range(len(values)))
        ax.set_xticklabels(labels, rotation=90)

        # Ustawienia tytułu i etykiet osi
        plt.title('Zmiana struktury kapitałowej generacja: ' + generacja)
        plt.xlabel('Kategorie')
        plt.ylabel('Zmiana wartości')
        fig.set_figheight(18)
        plt.tight_layout()

        # Wyświetlenie wykresu
        plt.show()


class DNA:
    dnaLength = 0
    dnaCode = []

    def __init__(self, dnaLength: int, dnaCode=[], structure_delta: StructureDelta = None):
        self.dnaLength = dnaLength
        if structure_delta:
            dnaCode = [0 for i in range(dnaLength)]
            nonCurrentAssets = structure_delta.nonCurrentAssets
            currentAssets = structure_delta.currentAssets
            equityShareholdersOfTheParent = structure_delta.equityShareholdersOfTheParent
            nonCurrentLiabilities = structure_delta.nonCurrentLiabilities
            currentLiabilities = structure_delta.currentLiabilities
            for index in range(dnaLength):
                if index % 5 == 0:
                    if nonCurrentAssets < 0:
                        dnaCode[index] += random.uniform(nonCurrentAssets, 0)
                        nonCurrentAssets += dnaCode[index]
                    else:
                        dnaCode[index] += random.uniform(0, nonCurrentAssets)
                        nonCurrentAssets -= dnaCode[index]
                elif index % 5 == 1:
                    if currentAssets < 0:
                        dnaCode[index] += random.uniform(currentAssets, 0)
                        currentAssets += dnaCode[index]
                    else:
                        dnaCode[index] += random.uniform(0, currentAssets)
                        currentAssets -= dnaCode[index]
                elif index % 5 == 2:
                    if equityShareholdersOfTheParent < 0:
                        dnaCode[index] += random.uniform(equityShareholdersOfTheParent, 0)
                        equityShareholdersOfTheParent += dnaCode[index]

                    else:
                        dnaCode[index] += random.uniform(0, equityShareholdersOfTheParent)
                        equityShareholdersOfTheParent -= dnaCode[index]

                elif index % 5 == 3:
                    if nonCurrentLiabilities < 0:
                        dnaCode[index] += random.uniform(nonCurrentLiabilities, 0)
                        nonCurrentLiabilities += dnaCode[index]

                    else:
                        dnaCode[index] += random.uniform(0, nonCurrentLiabilities)
                        nonCurrentLiabilities -= dnaCode[index]
                elif index % 5 == 4:
                        if currentLiabilities < 0:
                            dnaCode[index] = random.uniform(currentLiabilities, 0)
                            nonCurrentLiabilities += dnaCode[index]
                        else:
                            dnaCode[index] = random.uniform(0, currentLiabilities)
                            nonCurrentLiabilities -= dnaCode[index]
        self.dnaCode=dnaCode


    def returnDeltaStructure(self):
        nonCurrentAssets = 0
        currentAssets = 0
        equityShareholdersOfTheParent = 0
        nonCurrentLiabilities = 0
        currentLiabilities = 0
        for index, value in enumerate(self.dnaCode):
            if index % 5 == 0:
                nonCurrentAssets += value
            elif index % 5 == 1:
                currentAssets += value
            elif index % 5 == 2:
                equityShareholdersOfTheParent += value
            elif index % 5 == 3:
                nonCurrentLiabilities += value
            elif index % 5 == 4:
                currentLiabilities += value
        return StructureDelta(nonCurrentAssets, currentAssets, equityShareholdersOfTheParent, nonCurrentLiabilities,
                              currentLiabilities)

    def __mul__(self, other):
        if self.dnaLength != other.dnaLength:
            raise Exception("Crossing ERROR - non equal length")
        crossPoint = int(random.randint(0, self.dnaLength))
        result = self.dnaCode[:crossPoint] + other.dnaCode[crossPoint + 1:]
        return DNA(self.dnaLength, result)


class CompanyStructure:
    startNonCurrentAssets = 0
    startCurrentAssets = 0
    startEquityShareholdersOfTheParent = 0
    startNonCurrentLiabilities = 0
    startCurrentLiabilities = 0

    def __init__(self, startNonCurrentAssets, startCurrentAssets, startEquityShareholdersOfTheParent,
                 startNonCurrentLiabilities, startCurrentLiabilities):
        self.startNonCurrentAssets = startNonCurrentAssets
        self.startCurrentAssets = startCurrentAssets
        self.startEquityShareholdersOfTheParent = startEquityShareholdersOfTheParent
        self.startNonCurrentLiabilities = startNonCurrentLiabilities
        self.startCurrentLiabilities = startCurrentLiabilities

    def __mul__(self, other: StructureDelta):
        return CompanyStructure(
            self.startNonCurrentAssets * other.nonCurrentAssets,
            self.startCurrentAssets * other.currentAssets,
            self.startEquityShareholdersOfTheParent * other.equityShareholdersOfTheParent,
            self.startNonCurrentLiabilities * other.nonCurrentAssets,
            self.startCurrentLiabilities * other.currentAssets,
        )

    def visualize(self):
        # Dane do tabeli
        labels = [
            'Aktywa trwałe',
            'Aktywa obrotowe',
            'Kapitał własny udziałowców podmiotu dominującego',
            'Zobowiązania długoterminowe',
            'Zobowiązania krótkoterminowe'
        ]
        values = [self.startNonCurrentAssets, self.startCurrentAssets, self.startEquityShareholdersOfTheParent,
                  self.startNonCurrentLiabilities, self.startCurrentLiabilities]

        # Tworzenie DataFrame z danymi
        df = pd.DataFrame({'Wartości': values}, index=labels)

        # Wyświetlanie tabeli
        fig, ax = plt.subplots()
        fig.set_figwidth(10)  # Zwiększenie szerokości figury
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.2, 1.2)
        table.auto_set_column_width([0])  # Dostosowanie szerokości pierwszej kolumny
        plt.tight_layout()
        # Wyświetlenie tabeli
        plt.show()
