# ref: https://www.youtube.com/watch?v=yvHrNlAF0Y0
from pynput.keyboard import Key, Listener
import os
import csv
import logging
import time
import datetime
import Converter as converter

# define test modes
test1 = 1
test1Phase2 = 11
test2 = 2
normalMode = 3


class KeyLogger:
    def __init__(self, usrID=None, usrName=None, fernetClass=None):
        self.log_dir = ""
        self.res_dir = "Results/"
        self.current_user_id = usrID
        self.current_user_name = usrName
        self.fernet_Class = fernetClass

    def activateKeyLogger(self, testMode=None):
        print("Start Recording\n")

        if testMode is normalMode:
            # Remove all handlers associated with the root logger object.
            # To write new logging file
            for handler in logging.root.handlers[:]:
                logging.root.removeHandler(handler)
            # exists = os.path.isfile(self.res_dir + str(datetime.datetime.now()))
            filename = (str(datetime.datetime.now()))
            filename = filename.replace(' ', '_')
            filename = filename.replace(':', '.')
            logging.basicConfig(filename=(self.res_dir + filename + ".txt"), level=logging.DEBUG,
                                format='%(asctime)s: %(message)s:')
        else:
            exists = os.path.isfile(self.log_dir + "key_log.txt")
            if exists:
                os.remove(self.log_dir + "key_log.txt")
            logging.basicConfig(filename=(self.log_dir + "key_log.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s:')

        start = time.time()
        if testMode is test1 or testMode is test1Phase2:
            testTime = 15

        def on_press(key):
            end = time.time()
            print(end-start)
            # region Test 2
            if testMode is test2:
                if key == Key.esc:
                    print("Pressed ESC! [= Test 2 =]")
                    logging.shutdown()
                    converter.convertToCSV(self.log_dir + "key_log.txt")
                    avgSpeed = converter.convertSecToList(self.log_dir + "key_log.txt")
                    print("Average speed test: {0} msec".format(avgSpeed))
                    self.fernet_Class.decrypt_file("resultsFile.csv")
                    with open("resultsFile.csv", 'a', newline='') as resultFile:
                        writer = csv.writer(resultFile)
                        writer.writerow(["Test 2 Result", str(datetime.datetime.now()), "Average Speed:", avgSpeed])
                    self.fernet_Class.encrypt_file("resultsFile.csv")
                    return False
            # endregion
            # Test 1
            if (testMode is test1 or testMode is test1Phase2) and (end-start) >= testTime:
                print("Times Up [= Test 1 =]")
                logging.shutdown()
                converter.convertToCSV(self.log_dir + "key_log.txt")
                avgSpeed = converter.convertSecToList(self.log_dir + "key_log.txt")
                print("Average speed test: {0} msec".format(avgSpeed))
                self.fernet_Class.decrypt_file("resultsFile.csv")
                with open("resultsFile.csv", 'a', newline='') as resultFile:
                    writer = csv.writer(resultFile)
                    if testMode is test1:
                        writer.writerow(["Test 1 Result", str(datetime.datetime.now()), "Average Speed:", avgSpeed])
                    elif testMode is test1Phase2:
                        writer.writerow(["Test 1 Phase 2 Result", str(datetime.datetime.now()), "Average Speed:", avgSpeed])
                self.fernet_Class.encrypt_file("resultsFile.csv")
                return False
            # Normal Mode
            logging.info(str(key))
            if key == Key.esc:
                print("Pressed ESC! [= Normal Mode =]")
                logging.shutdown()
                converter.convertToCSV(self.res_dir + filename + ".txt")
                converter.encrypt_File_Data(self.res_dir + filename + ".txt", self.fernet_Class)
                avgSpeed = converter.convertSecToList(self.res_dir + filename + ".txt")
                # os.remove(self.res_dir + filename + ".txt")
                if avgSpeed != (-99):
                    converter.recordAvgSpeed(avgSpeed, filename, self.fernet_Class)
                    converter.recordAvgSpeedServer(self.current_user_id, avgSpeed, filename, self.fernet_Class)
                os.remove(self.res_dir + filename + ".txt")
                os.remove(self.res_dir + "ResultsCsv/" + filename + ".txt.csv")
                return False

        with Listener(on_press=on_press) as listener:
            listener.join()

    def getFile(self):
        return self.log_dir + "key_log.txt"

    def set_User(self, usrName, usrID, fernetClass = None):
        self.current_user_name = usrName
        self.current_user_id = usrID
        self.fernet_Class = fernetClass
