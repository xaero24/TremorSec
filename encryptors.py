from hashlib import sha1, sha256
import random, mailing
import smtplib, ssl

def enc (data, usrname):
    """
    Encryption is done locally in SHA-256 key.
    The produced hash is to be sent to the server and is meant to be stored there.
    Salt is used in the form of first 15 chars of the username's SHA1 hash.
    The intercepted message is not likely to be decrypted in this way.
    """
    key = (sha1(usrname.encode('utf-8')).hexdigest())[0:15]
    return sha256((data + key).encode('utf-8')).hexdigest()

def check (data, usrname, cipher):
    """
    The user is passed through two verification steps:
    1. Password is checked according to the username.
    2. E-mail verification code is requested.
    """
    if cipher == enc(data, usrname):
        print("A code will be sent to your eMail with a verification code...")
        verifier = random.randint(10000,99999)
        #Pull user email from server - TBI (stump is used now)
        # PULL HERE
        #send email verification
        mailing.sender(verifier)
        receivedCode = int(input("Your code here: "))
        if receivedCode == verifier:
            print("Access granted!")
        else:
            print("Wrong code")
    else:
        print("Wrong password or username")