from KeyLogger import KeyLog
import csv
import re
import os

Log = KeyLog()
Log.activateLogging()


def convertToCSV(path):
    with open(path, 'r') as in_file:
        # stripped = (line.strip() for line in in_file)
        # lines = (line.split(",") for line in stripped if line)
        # out_file = open(path + ".csv", 'w', newline="")
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


def reset():
    txt = open(Log.getFile(), 'w')
    csv = open(Log.getFile() + ".csv", 'w')
    txt.close()
    csv.close()

convertToCSV(Log.getFile())

option = input("Reset? y/n \n")
if option == 'y':
    reset()
else:
    print("exit")



