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

        lost_followings = (set(old_followings) - set(followings))
        lost_followers = (set(old_followers) - set(followers))

        fans = (set(followers) - set(followings))

        print("Select options : ")
        while(True):
            print("1: Not Follow Back \n2: New Following \n3: New Followers \n4: Lost Followers \n5: Lost Followings \n6. Fans \n7: Exit")
            option = int(input())
            if(option == 1):
                print("Not Follow back: ")
                not_follow_back = (set(followings) - set(followers))
                print(len(not_follow_back))
                for users in not_follow_back:
                    print(users)
            elif(option == 2):
                print("New Followings: ")
                print(len(new_followings))
                for users in new_followings:
                    print(users)
            elif(option == 3):
                print("New Followers: ")
                print(len(new_followers))
                for users in new_followers:
                    print(users)
            elif(option == 4):
                print("Lost Followers: ")
                print(len(lost_followers))
                for users in lost_followers:
                    print(users)
            elif(option == 5):
                print("Lost Followings: ")
                print(len(lost_followings))
                for users in lost_followings:
                    print(users)
            elif(option == 6):
                print("Fans:")
                print(len(fans))
                for users in fans:
                    print(users)
            elif(option == 7):
                break
            else:
                print("Enter a valid option!")

        for names in new_followers:
            try:
                my_cursor.execute("INSERT INTO follower_following(follower_id, following_id) VALUES(%s, %s)", (names, user_id,))
            except:
                continue

        for names in new_followings:
            try:
                my_cursor.execute("INSERT INTO follower_following(follower_id, following_id) VALUES(%s, %s)", (user_id, names,))
            except:
                continue

        for names in lost_followers:
            try:
                my_cursor.execute("delete from follower_following where following_id = %s and follower_id = %s", (user_id, names,))
            except:
                continue

        for names in lost_followings:
            try:
                my_cursor.execute("delete from follower_following where following_id = %s and follower_id = %s", (names, user_id,))
            except:
                continue

        mydb.commit()

    else:
        print("You are a new user")

        my_cursor.execute("insert into users(user_id) value(%s)", (user_id,))

        print("Select Option: \n1.Not Follow Back \n2.Fans \n3.Exit")
        while(True):
            option = int(input())
            if(option == 1):
                print("Not Follow back: ")
                not_follow_back = (set(followings) - set(followers))
                print(len(not_follow_back))
                for users in not_follow_back:
                    print(users)
            elif(option == 2):
                print("Fans: ")
                fans = (set(followers) - set(followings))
                print(len(fans))
                for users in fans:
                    print(users)
            elif(option == 3):
                break
            else:
                print("Enter valid option!")

            for names in followers:
                try:
                    my_cursor.execute("INSERT INTO follower_following(follower_id, following_id) VALUES(%s, %s)", (names, user_id,))  
                except:
                    continue

            for names in followings:
                try:
                    my_cursor.execute("INSERT INTO follower_following(follower_id, following_id) VALUES(%s, %s)", (user_id, names,))
                except:
                    continue
            
            mydb.commit()

    

