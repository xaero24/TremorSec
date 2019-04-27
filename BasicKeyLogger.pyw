# ref: https://www.youtube.com/watch?v=yvHrNlAF0Y0
from pynput.keyboard import Key, Listener
import os, csv
import logging
import time
import Converter as converter

# define test modes
test1 = 1
test2 = 2


class KeyLogger:
    def __init__(self):
        self.log_dir = ""

    def activateKeyLogger(self, testMode=None):
        print("Start Recording\n")
        if testMode is None:
            print(testMode)
        else:
            print("TestMode")

        exists = os.path.isfile(self.log_dir + "key_log.txt")
        if exists:
            os.remove(self.log_dir + "key_log.txt")

        logging.basicConfig(filename=(self.log_dir + "key_log.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s:')

        start = time.time()
        if testMode is test1:
            testTime = 15

        def on_press(key):
            end = time.time()
            print(end-start)
            # Test 2
            if testMode is test2:
                if key == Key.esc:
                    logging.shutdown()
                    converter.convertToCSV(self.log_dir + "key_log.txt")
                    avgSpeed = converter.convertSecToList(self.log_dir + "key_log.txt")
                    print("Average speed test: {0} msec".format(avgSpeed))
                    with open("resultsFile.csv", 'a') as resultFile:
                        writer = csv.writer(resultFile)
                        writer.writerow(["Test 1 Result", "Average Speed:", avgSpeed])
                    return False
            # Test 1
            if testMode is test1 and (end-start) >= testTime:
                logging.shutdown()
                converter.convertToCSV(self.log_dir + "key_log.txt")
                avgSpeed = converter.convertSecToList(self.log_dir + "key_log.txt")
                print("Average speed test: {0} msec".format(avgSpeed))
                with open("resultsFile.csv", 'a') as resultFile:
                    writer = csv.writer(resultFile)
                    writer.writerow(["Test 2 Result", "Average Speed:", avgSpeed])
                return False
            logging.info(str(key))
            if key == Key.esc:
                logging.shutdown()
                return False

        with Listener(on_press=on_press) as listener:
            listener.join()

    def getFile(self):
        return self.log_dir + "key_log.txt"
