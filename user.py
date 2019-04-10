from hashlib import sha1, sha256
import random, mailing
import smtplib, ssl, datetime

class User:
    def __init__(self):
        self.firstName = input("First name: ")
        self.lastName = input("Last name: ")
        self.dateOfBirth = datetime.datetime.strptime(
            input("Day of birth (2 digits): ") + '-' + 
            input("Month of birth (2 digits): ") + '-' + 
            input("Year of birth (4 digits): "), 
            '%d-%m-%Y'
        ).date()
        self.email = input("E-mail address: ")
        self.username = input("Username: ")
        pass1 = input("Password: ")
        pass2 = input("Repeat password: ")
        while pass1 != pass2:
            print("Passwrds don't match, try again.")
            pass1 = input("Password: ")
            pass2 = input("Repeat password: ")
        self.password = self.enc(pass1, self.username) #To be removed/modified. Info is sent to a remote database.
        
    def enc (self, passwd, usrname):
        """
        Encryption is done locally in SHA-256 key.
        The produced hash is to be sent to the server and is meant to be stored there.
        Salt is used in the form of first 15 chars of the username's SHA1 hash.
        The intercepted message is not likely to be decrypted in this way.
        """
        key = (sha1(usrname.encode('utf-8')).hexdigest())[0:15]
        return sha256((passwd + key).encode('utf-8')).hexdigest()

    def check (self, passwd, usrname):
        """
        The user is passed through two verification steps:
        1. Password is checked according to the username.
        2. E-mail verification code is requested.
        """
        if self.enc(passwd, usrname) == self.password: #To be modified, SHA is pulled from server.
            print("A code will be sent to your eMail with a verification code...")
            verifier = random.randint(10000,99999)
            #Pull user email from server - TBI (stump is used now)
            # PULL HERE
            #send email verification
            mailer = mailing.Mailing(self.email)
            mailer.sender(verifier)
            receivedCode = int(input("Your code here: "))
            if receivedCode == verifier:
                print("Access granted!")
            else:
                print("Wrong code")
        else:
            print("Wrong password or username")