import pyodbc
import sha1


class connection(object):
    def __init__(self):
        server = 'parki.database.windows.net'
        database = 'par'
        username = 'paradmin'
        password = 'Padmin13'
        self.cnxn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server}; SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        self.cursor = self.cnxn.cursor()

    def readAll(self):
        self.cursor.execute("SELECT * FROM dbPark")
        row = self.cursor.fetchone()
        times = []
        while row:
            times.append(row[2])
            row = self.cursor.fetchone()
        return times

    def wirteNL(self, dat, val):
        query = """INSERT INTO dbPark (date, avgSpeed) VALUES ('{0}',{1})""".format(dat, val)
        self.cursor.execute(query)
        self.cnxn.commit()

    def readUsers(self):
        values = dict()
        query = """SELECT * FROM dbUser"""
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        while row:
            values[row[1]] = row[2]
            row = self.cursor.fetchone()
        return values

    def signUp_User(self, username, password):
        try:
            Hash_Password = sha1.shaControl(password)  # Creating Hashing module
            Hash_Password.sha1()  # Hashing the password
            query = """INSERT INTO dbUser (UserName, HashPass) VALUES ('{0}','{1}')""".format(username, Hash_Password.password)
            self.cursor.execute(query)
            self.cnxn.commit()
            print("[!] Added User:\nUser Name: {0} \nHash Password: {1}".format(username, Hash_Password.password))
            return True
        except:
            print("Error Adding new User")
            return False


# cont = connection()
# username = "tzvi"
# password = "1234A"
# cont.signUp_User(username, password)

