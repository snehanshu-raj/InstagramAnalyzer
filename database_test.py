import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Monu@1291",
)

my_cursor = mydb.cursor()

my_cursor.execute("SHOW DATABASES")
for i in my_cursor:
    if(i[0] == "lab2"):
        print("database present")


print(mydb)