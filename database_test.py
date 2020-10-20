import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Monu@1291",
)

my_cursor = mydb.cursor(buffered=True)

my_cursor.execute("use instagram")

my_cursor.execute("select * from users")


# for i in my_cursor:
#     if(i[0] == "srj.monuuu"):
#         print("p")
#     print(i)

user_id = "srj.doodler"
names = 'nba'
my_cursor.execute("delete from follower_following where following_id = %s and follower_id = %s", (names, user_id,))

# for i in my_cursor:
#     print(i[0])
# user_id = "srj.monuu"
# my_cursor.execute("insert into users(user_id) value(%s)", (user_id,))
# my_cursor.execute("SHOW DATABASES")
# for i in my_cursor:
#     if(i[0] == "lab2"):
#         print("database present")
#     else:
#         print("Not")

# user_id = "srj.snehanshu"
# my_cursor.execute("CREATE DATABASE " + user_id + "")
# my_cursor.execute("USE " + user_id + "")
# my_cursor.execute("CREATE TABLE followers (id varchar(100))")
# my_cursor.execute("CREATE TABLE followings (id varchar(100))")

# followers = ["sedg", "aegssr"]
# for names in followers:
#     print(names)
#     my_cursor.execute("INSERT INTO followers(id) VALUES(%s)", (names,))
mydb.commit()
