import pyodbc

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

#c = connection()
#print(c.wirteNL("ajhvyah", 234.34))