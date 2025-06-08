import sqlite3  

dataBase = "dataBase.db"
connection = sqlite3.connect(dataBase)
cursor = connection.cursor()
    

def buildSQLInsert(table, rows, data):
    cursor.execute('''  
                   INSERT INTO ?
                   (?)
                   VALUES(?)''',
                   (table, rows, data))
    connection.commit()

def buildSQLUpdate(table, rows, id):
    cursor.execute('''  
                   UPDATE ?
                   SET ?
                   WHERE ID = ?''',
                   (table, rows, id))
    connection.commit()

def buildSQLDelete(table, id):
    cursor.execute('''  
                   DELETE FROM ?
                   WHERE ID = ?''',
                   (table, id))
    connection.commit()
    
def buildSQLSelect(table, id):
    cursor.execute('''  
                   SELECT *
                   FROM ?
                   WHERE ID = ?''',
                   (table, id))
    return cursor.fetchall()