import csv
import re
import time
from Coordinator import Coordinator
import fernetAES
from cryptography.fernet import InvalidToken
import os
# define
idleTime = 15000
c = Coordinator()


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
    try:
        avgSpeed = sum(subSeconds)/len(subSeconds)
    except:
        print("No Data recorded")
        return -99
    return avgSpeed


def recordAvgSpeed(avgSpeed, stamp, encryptAES):
    path = "Results/AvgSpeeds.csv"
    exists = os.path.isfile("Results/AvgSpeeds.csv")
    if exists:
        encryptAES.decrypt_file(path)
    with open(path, 'a', newline="") as outFile:
        writer = csv.writer(outFile)
        writer.writerow([stamp, avgSpeed])
    encryptAES.encrypt_file(path)


def recordAvgSpeedServer(userId, avgSpeed, stamp, fernet):
    avgSpeed = fernet.fernet_encrypt(str(avgSpeed)).decode()
    c.tryCommit(userId, stamp, avgSpeed)


def encrypt_File_Data(path, encryptAES):
    with open(path, 'rb') as in_file:
        data = in_file.read()
        subPath = path.replace('/', "/Encrypted/")
        with open(subPath, 'wb') as out_file:
            out_file.write(encryptAES.fernet_Key_obj.encrypt(data))


def decrypt_File_Data(path, encryptAES):
    with open(path, 'rb') as in_file:
        data = in_file.read()
        try:
            data = encryptAES.fernet_Key_obj.decrypt(data).decode()
        except InvalidToken:
            print("[ERROR] Bad Key Encryption")
            return
        with open(path + '_decrypted.txt', 'w', newline="") as out_file:
            out_file.write(data)


# region  Functionality Test
# c = fernetAES.fernet_Encryption('oP6zdSCHd1JH0RFcvC8OKpSplrecJTd9Xw4lSGfFov4=')
# decrypt_File('Results/Encrypted/2019-06-08_01.44.24.371549.txt', c)
# endregion
