import sqlite3  

dataBase = "dataBase.db"
connection = sqlite3.connect(dataBase)
cursor = connection.cursor()
    

def buildSQLInsert(table, rows, data):
    """
    Build a SQL Insert command given a table, rows, and data to insert

    :param table: The table to insert data into
    :param rows: The row(s) to insert data into
    :param data: The data to be inserted
    """
    cursor.execute('''  
                   INSERT INTO ?
                   (?)
                   VALUES(?)''',
                   (table, rows, data))
    connection.commit()

def buildSQLUpdate(table, rows, id):
    """
    Build a SQL Update command given a table, rows, and id to update

    :param table: The table to update
    :param rows: The row(s) to update
    :param id: The ID of the row to update
    """
    cursor.execute('''  
                   UPDATE ?
                   SET ?
                   WHERE ID = ?''',
                   (table, rows, id))
    connection.commit()

def buildSQLDelete(table, id):
    """
    Build a SQL Delete command given a table and an id to delete a specific row

    :param table: The table from which to delete data
    :param id: The ID of the row to be deleted
    """

    cursor.execute('''  
                   DELETE FROM ?
                   WHERE ID = ?''',
                   (table, id))
    connection.commit()
    
def buildSQLSelect(table, id):
    """
    Build a SQL Select command to retrieve all columns from a specific row in a table by ID.

    :param table: The table to select data from
    :param id: The ID of the row to retrieve
    :return: A list of tuples containing the data from the selected row
    """

    cursor.execute('''  
                   SELECT *
                   FROM ?
                   WHERE ID = ?''',
                   (table, id))
    return cursor.fetchall()