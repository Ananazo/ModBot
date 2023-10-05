import mysql.connector
import os
def sqlfunc (sql, val):
    mydb = mysql.connector.connect(
                host=os.getenv('HOST'),
                user=os.getenv('USER'),
                password=os.getenv('PASS'),
                database="ModBot"
            )

    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()