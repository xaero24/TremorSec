import encryptAndCheck as pak1
from hashlib import sha1

"""
Takes a username and a password and encryprs it.
The hash is generated and pulled from the server by username - implement.
Password is compared to locally generated hash - implement.

Unresolved imports - might be VSCode problems?
"""

usrname = input("Enter username: ")
passwd = input("Enter password: ")

print(pak1.enc(passwd, usrname))
