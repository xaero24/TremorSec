import conjnk as conClass

class Coordinator:
    def __init__(self):
        #Use connection strings
        self.con = None
        self.log = {}

    def tryCommit(self, date, value):
        try:
            self.con = conClass()
            self.con.wirteNL(date, value)
            print("Connection Succeded \n")
            if(len(self.log) > 1):
                for (d, v) in self.log:
                    self.con.wirteNL(d, v)
                    self.log.pop(d)
        except:
            print("Connection failed, try again later\n")
            self.log[date] =  value
            return -1
        
