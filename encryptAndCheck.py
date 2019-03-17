from hashlib import sha1, sha256

"""
Encryption is done locally in SHA-256 key.
The produced hash is to be sent to the server and is meant to be stored there.
Salt is used in the form of first 15 chars of the username's SHA1 hash.
The intercepted message is not likely to be decrypted in this way.
"""

def enc (data, usrname):
    key = (sha1(usrname.encode('utf-8')).hexdigest())[0:15]
    return sha256((data + key).encode('utf-8')).hexdigest()

def check (data, usrname, cipher):
    return cipher == enc(data, usrname)

