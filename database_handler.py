import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Monu@1291",
)

my_cursor = mydb.cursor(buffered=True)

def updating_user_info(user_id, followers, followings):   
    already_a_user = False

    my_cursor.execute("USE instagram")

    my_cursor.execute("select * from users")

    for user in my_cursor:
        if(user[0] == user_id):
            already_a_user = True
            break
    
    if(already_a_user == True):
        print("You are already a user")
        old_followings = []
        old_followers = []

        my_cursor.execute("select following_id from follower_following where follower_id = %s", (user_id,))
        for i in my_cursor:
            old_followings.append(i[0])
        
        my_cursor.execute("select follower_id from follower_following where following_id = %s", (user_id,))
        for i in my_cursor:
            old_followers.append(i[0])
        
        new_followings = (set(followings) - set(old_followings))
        new_followers = (set(followers) - set(old_followers))

        print(new_followers)
        print(new_followings)

        lost_followings = (set(old_followings) - set(followings))
        lost_followers = (set(old_followers) - set(followers))

        print(lost_followers)
        print(lost_followings)

        for names in new_followers:
            my_cursor.execute("INSERT INTO follower_following(follower_id, following_id) VALUES(%s, %s)", (names, user_id,))

        for names in new_followings:
            my_cursor.execute("INSERT INTO follower_following(follower_id, following_id) VALUES(%s, %s)", (user_id, names,))

        for names in lost_followers:
            my_cursor.execute("delete from follower_following where following_id = %s and follower_id = %s", (user_id, names,))
        
        for names in lost_followings:
            my_cursor.execute("delete from follower_following where following_id = %s and follower_id = %s", (names, user_id,))

        mydb.commit()
    else:
        print("You are a new user")

        my_cursor.execute("insert into users(user_id) value(%s)", (user_id,))

        for names in followers:
            my_cursor.execute("INSERT INTO follower_following(follower_id, following_id) VALUES(%s, %s)", (names, user_id,))  

        for names in followings:
            my_cursor.execute("INSERT INTO follower_following(follower_id, following_id) VALUES(%s, %s)", (user_id, names,))

        print("Not Follow back: ")
        nfb = (set(followings) - set(followers))
        print(nfb)
        
        mydb.commit()
