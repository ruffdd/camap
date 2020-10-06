import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  database="camap",
  user="camap",
  password="camaper"
)

cursor = mydb.cursor()

def tables():
    cursor.execute("show tables;")
    return cursor.fetchall()

if len(tables()) == 0 :
    cursor.execute("CREATE TABLE buildings (id VARCHAR(20) PRIMARY KEY);")

