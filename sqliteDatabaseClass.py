import sqlite3


class FaceRecogDatabase(object):

    def __init__(self, name = "test"):
        self.name = name
        print(name)
        self.connection = sqlite3.connect(f"{name}.db")
        self.cursor = self.connection.cursor()

    def __repr__(self):
        return (f"DB name: {self.name}\nConnection: {self.connection}")

        
    def terminate(self):
        self.connection.close()

    def execute(self, sqlString):
        val = self.cursor.execute(sqlString)
        return val

    
    def createTable(self, tableName:str, tableAttributes:dict):
        val = self.execute(f"create table {tableName} ( {retDictStrings(tableAttributes)})")
        return val
    
    def insert(self, tableName:str, values:list):
        valuesString = turnListtoSet(values)
        # print(valuesString)                   #dev check
        val = self.execute(f"insert into {tableName} values {valuesString}")
        return val
    
    def insertMany(self, tableName:str, valuesListOfSets:list):
        val = self.cursor.executemany(f"insert into {tableName} values (?,?,?)", valuesListOfSets)
        return val
    
def retDictStrings(aDict: dict):
    """
    Expects: tableAttributes in format (sql data types): {"Fname": "varchar(256)", "ID": "integer"}
    """
    retString = ""
    for item in aDict:
        retString += f"{item} {aDict[item]},"
    return retString.strip(",")

def turnListtoSet(argList:list):
    retString = "("
    for item in argList:
        if type(item) == str:
            retString += f"\'{item}\', "
        else:
             retString += f"{item}, "
    retString = retString.strip(", ") #remove trailing ','
    retString += ")"
    return retString


if __name__ == "__main__":

    print("Testing FaceRecogDatabase class")

    testDB = FaceRecogDatabase("Test School Database")
    print(testDB)
    # Create tables
    try:
        testDB.createTable("Students", {"Name": "varchar(30)", "ID": "integer"})
    except Exception as e:
        print(e,"Table already Exists")
        

    # Insertions
    # try:
    #     testDB.insert("Students", ["Olasubomi Badiru", 1])
    #     testDB.insert("Students", ["Monisola Badiru", 2])

    # except:
    #     print("Values already present")

    print("\nShowing values in table- Students")
    for row in testDB.execute("select * from Students"):
        print(row)
    
    testDB.terminate()