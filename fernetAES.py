from cryptography.fernet import Fernet
import os
from cryptography.fernet import InvalidToken

"""
Uses implementation of AES encryption using 128-bit key.
For authentication uses SHA-256
"""


class fernet_Encryption:
    def __init__(self, key):
        self.key = key
        self.fernet_Key_obj = Fernet(key)

    def fernet_encrypt(self, message):
        return self.fernet_Key_obj.encrypt(message.encode())

    def fernet_decrypt(self, message):
        return self.fernet_Key_obj.decrypt(message).decode()

    def encrypt_file(self, path):
        with open(path, 'rb') as in_file:
            data = in_file.read()
            with open(path, 'wb') as out_file:
                out_file.write(self.fernet_Key_obj.encrypt(data))

    def decrypt_file(self, path):
        with open(path, 'rb') as in_file:
            data = in_file.read()
            data = self.fernet_Key_obj.decrypt(data).decode()
            # try:
            #     data = self.fernet_Key_obj.decrypt(data).decode()
            # except InvalidToken:
            #     print("[ERROR] Bad Key Encryption")
            #     return False
            with open(path, 'w', newline="") as out_file:
                out_file.write(data)
            return True


def get_Key():
    return Fernet.generate_key()


# region Test Run
# key = Fernet.generate_key()
# message = "secret Encoded Message".encode()
# f = Fernet(key)
# encrypted = f.encrypt(message)
# print(encrypted)
#
# decrypted = f.decrypt(encrypted).decode()
# print(decrypted)
# print()
# c = fernet_Encryption('oP6zdSCHd1JH0RFcvC8OKpSplrecJTd9Xw4lSGfFov4=')
# c.decrypt_file('Results/AvgSpeeds.csv')
# print()
# endregion
