from KeyLogger import KeyLog
import csv
import re

Log = KeyLog()
Log.activateLogging()


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


def reset():
    """
    Resets the files to empty ones for new data
    :return:
    """
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



