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
        self.user = None

    def createPlot(self, current_User):
        global currentValues
        self.user = current_User  # Sets User Class obj
        vals = getMaxMinTests(self)
        self.max = vals[0][3]
        self.min = vals[1][3]
        if self.mode is file:
            currentValues = getValues(self)
        elif self.mode is server:
            currentValues = getServerValues_User(self.user.user_server_id, self.user)
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


def getMaxMinTests(plot):
    exists = os.path.isfile("resultsFile.csv")
    if exists:
        plot.user.fernet_class.decrypt_file("resultsFile.csv")
        with open("resultsFile.csv", 'r') as cfile:
            reader = csv.reader(cfile, delimiter=',')
            vals = [row for idx, row in enumerate(reader) if idx in (2, 3, 4)]
            print(vals)
            for row in vals:
                row[3] = float(row[3])
            plot.user.fernet_class.encrypt_file("resultsFile.csv")
            return vals


def getValues(plot):
    exists = os.path.isfile("Results/AvgSpeeds.csv")
    if exists:
        if plot.user.fernet_class.decrypt_file("Results/AvgSpeeds.csv"):
            vals = list()
            with open("Results/AvgSpeeds.csv", 'r') as file:
                reader = csv.reader(file, delimiter=',')
                for line in reader:
                    vals.append(float(line[1]))
            plot.user.fernet_class.encrypt_file("Results/AvgSpeeds.csv")
            return vals


def getServerValues():
    serverConnection = conct.connection()
    vals = serverConnection.readAll()
    return vals


def getServerValues_User(userId, userObj):
    serverConnection = conct.connection()
    vals = serverConnection.read_UserId(userId)
    # Decrypt Values and convert back to float format for the plot
    for x in range(len(vals)):
        vals[x] = float(userObj.fernet_class.fernet_decrypt(vals[x].encode()))
    return vals
