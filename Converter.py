import csv
import re


def convertToCSV(path):
    """
    converts the key log txt to csv data base for later use
    :param name of the key log file:
    :return:
    """
    with open(path, 'r') as in_file:
        with open(path + ".csv", 'w', newline="") as out_file:
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
        if x != secLen - 1:
            if seconds[x] <= 60000 < seconds[x + 1]:
                subSeconds.append(60000 + (seconds[x+1] - seconds[x]))
            else:
                subSeconds.append(seconds[x+1] - seconds[x])
    avgSpeed = sum(subSeconds)/len(subSeconds)
    return avgSpeed
# option = input("Reset? y/n \n")
# if option == 'y':
#     reset()
# else:
#     print("exit")



