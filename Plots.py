import matplotlib.pyplot as plt
import os
import csv
import connector as conct

file = 0
server = 1


class PlotCreate:
    def __init__(self, mode=file):
        self.max = None
        self.min = None
        self.numOfTest = None
        self.ylabel = "Avg Speed"
        self.xlabel = "Test no"
        self.mode = mode

    def createPlot(self):
        vals = getMaxMinTests()
        self.max = vals[0][3]
        self.min = vals[1][3]
        if self.mode is file:
            currentValues = getValues()
        elif self.mode is server:
            currentValues = getServerValues()
        if currentValues is not None:
            currentValues.insert(0, vals[2][3])
        else:
            currentValues = list()
            currentValues.append(vals[2][3])
        self.numOfTest = len(currentValues)

        if currentValues[0] > self.max :
            self.max = currentValues[0] + (currentValues[0] - self.max)
            print("[Plot] Max changed. Test 2 greater than Test1")
        maxValueLine = list()
        for _ in range(self.numOfTest + 3):
            maxValueLine.append(self.max)
        plt.plot(maxValueLine, linestyle='-.', color='r')

        minValueLine = list()
        for _ in range(self.numOfTest + 3):
            minValueLine.append(self.min)
        plt.plot(minValueLine, linestyle='-.', color='r')

        baseLine = list()
        for _ in range(self.numOfTest + 3):
            baseLine.append(vals[2][3])
        plt.plot(baseLine, linestyle='--', color='g')

        xAxis = list()
        for x in range(1, self.numOfTest + 1):
            xAxis.append(x)
        plt.plot(xAxis, currentValues, color='b')

        plt.show()


def getMaxMinTests():
    exists = os.path.isfile("resultsFile.csv")
    if exists:
        with open("resultsFile.csv", 'r') as cfile:
            reader = csv.reader(cfile, delimiter=',')
            vals = [row for idx, row in enumerate(reader) if idx in (2, 3, 4)]
            print(vals)
            for row in vals:
                row[3] = float(row[3])
            return vals


def getValues():
    exists = os.path.isfile("Results/AvgSpeeds.csv")
    if exists:
        vals = list()
        with open("Results/AvgSpeeds.csv", 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for line in reader:
                vals.append(float(line[1]))
            return vals


def getServerValues():
    serverConnection = conct.connection()
    vals = serverConnection.readAll()
    return vals
