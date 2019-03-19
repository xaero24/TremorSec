from KeyLogger import KeyLog
import csv
import re
Log = KeyLog()
Log.activateLogging()


def convertToCSV(path):
    with open(path, 'r') as in_file:
        # stripped = (line.strip() for line in in_file)
        # lines = (line.split(",") for line in stripped if line)
        out_file = open(path + ".csv", 'w')
        writer = csv.writer(out_file, delimiter=',', quotechar='"')
        writer.writerow(('date', 'time[h]', 'time[m]', 'time[s]', 'pressed'))
        for line in in_file:
            curline = line
            curline = re.sub("\n", "", curline).split(" ")
            curline[1] = curline[1][:-1]
            curline[1] = curline[1].replace(':', " ").split(" ")
            curline[2] = curline[2].replace(':', " ")
            newline = [curline[0], curline[1][0], curline[1][1], curline[1][2], curline[2]]
            writer.writerow(newline)
        # with open(path + ".csv", 'w') as out_file:
        #     writer = csv.writer(out_file)
        #     writer.writerow(('date', 'time','pressed'))
        #     writer.writerows(lines)


convertToCSV(Log.getFile())



