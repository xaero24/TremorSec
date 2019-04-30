import csv
import re
import os

# define
idleTime = 15000


def convertToCSV(path):
    """
    converts the key log txt to csv data base for later use
    :param path:
    """
    with open(path, 'r') as in_file:
        subPath = path.replace('/', "/ResultsCsv/")
        with open(subPath + ".csv", 'w', newline="") as out_file:
            writer = csv.writer(out_file, delimiter=',', quotechar='"')
            writer.writerow(('date', 'time[h]', 'time[m]', 'time[s]', 'pressed'))
            for line in in_file:
                curline = line
                curline = re.sub("\n", "", curline).split(" ")
                curline[1] = curline[1][:-1]
                curline[1] = curline[1].replace(':', " ").split(" ")
                curline[2] = curline[2].replace(':', " ")
                curline[1][2] = curline[1][2].replace(',', "")
                newline = [curline[0], curline[1][0], curline[1][1], curline[1][2], curline[2]]
                writer.writerow(newline)


def reset(path):
    """
    Resets the files to empty ones for new data
    :return:
    """
    txt = open(path, 'w')
    csv = open(path + ".csv", 'w')
    txt.close()
    csv.close()


def convertSecToList(path):
    seconds = list()
    with open(path, 'r') as in_file:
        for line in in_file:
            line = line.split(':')
            line[2] = line[2].replace(',', '')
            seconds.append(int(line[2], 10))
    if len(seconds) % 2 != 0:
        secLen = len(seconds) - 1
    else:
        secLen = len(seconds)
    subSeconds = list()
    for x in range(secLen):
        if x != secLen - 1:  # checks if end of list
            if 40000 < seconds[x] <= 60000 and 0 <= seconds[x + 1] < 15000:  # checks if its a new second
                if not ((seconds[x + 1] - seconds[x] + 60000) > idleTime):
                    subSeconds.append(seconds[x+1] - seconds[x] + 60000)
            elif not (seconds[x+1] - seconds[x]) > idleTime:
                subSeconds.append(seconds[x+1] - seconds[x])
    avgSpeed = sum(subSeconds)/len(subSeconds)
    return avgSpeed


def recordAvgSpeed(avgSpeed, stamp):
    path = "Results/AvgSpeeds.csv"
    with open(path, 'a', newline="") as outFile:
        writer = csv.writer(outFile)
        writer.writerow([stamp, avgSpeed])

