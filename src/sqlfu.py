import mysql.connector
import os

mydb = None

def sqlfunc(sql, val):
    global mydb
    result = None
    try:
        if mydb is None or not mydb.is_connected():
            mydb = mysql.connector.connect(
                host=os.getenv('HOST'),
                user=os.getenv('USER'),
                password=os.getenv('PASS'),
                database="ModBot"
            )
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        if mycursor.with_rows:
            result = mycursor.fetchall()
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
    finally:
        if mycursor:
            mycursor.close()
        if mydb and mydb.is_connected():
            mydb.close()
    return result
def get_admin_role_id(guild):
    for role in guild.roles:
        if role.permissions.administrator:
            return role.id
    return None