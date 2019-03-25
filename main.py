import encryptors

"""
Takes a username and a password and encryprs it.
The hash is generated and pulled from the server by username - implement.
Password is compared to locally generated hash - implement.

Unresolved imports - might be VSCode problems?
"""
#Sign up or login here:

#Sign up - information sent to DB, right now it's a stump
usrname = input("Enter username: ")
passwd = input("Enter password: ")
print("Thanks!")
code = encryptors.enc(passwd, usrname) #sent to server with username

#Log in - mail pulled later in the process from the DB for 2-stage verification, right now it's a stump
a_usrname = input("Enter username: ")
a_passwd = input("Enter password: ")

encryptors.check(a_passwd, a_usrname, code)