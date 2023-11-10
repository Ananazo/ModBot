import mysql.connector
import os

mydb = None

def sqlfunc(sql, val):
    global mydb
    if mydb is None:
        mydb = mysql.connector.connect(
            host=os.getenv('HOST'),
            user=os.getenv('USER'),
            password=os.getenv('PASS'),
            database="ModBot"
        )
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()