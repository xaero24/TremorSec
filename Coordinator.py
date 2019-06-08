from connector import connection

"""
This class is coordinating all the traffic. We want to record
new avg speed value to the server so this coordinator checking if 
he can connect to the server and write the new value.
If he didnt succeed the class records the value so he can send
it later when he can connect so we will not loose data.
"""


class Coordinator:
    def __init__(self):
        # Use connection strings
        self.con = None
        self.log = {}

    def tryCommit(self, userId, date, value):
        """"Try commit the values if dont succeed saves the
            the values int the dictionary for later value send"""
        try:
            self.con = connection()
            print("Connection Succeed \n")
            if bool(self.log):
                for key in self.log:
                    self.con.writeNL(key, self.log[key])
                self.log = {}
            self.con.writeNL(userId, date, value)
            print("Sent Data to Serer !! [V]")
        except Exception as e:
            print(e)
            print("Connection failed, try again later\n")
            self.log[date] = value
            return -1
