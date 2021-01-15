#C:\Users\Snehanshu Raj\Downloads\chromedriver_win32\chromedriver.exe

from tqdm import tqdm
import database_handler
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time
import getpass

chromePath = r"C:\Users\Snehanshu Raj\Downloads\chromedriver_win32\chromedriver.exe"

driver = webdriver.Chrome(executable_path=chromePath)

driver.get('https://www.instagram.com/accounts/login/')

#logging in
logged_in = False

time.sleep(2)
user_id = input("Enter username or phone number: ")
driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[1]/div/label/input').send_keys(user_id)

time.sleep(2)
password = getpass.getpass()
driver.find_element_by_xpath('/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div/div[2]/div/label/input').send_keys(password)

credentials = False
time.sleep(2)
try:
    driver.find_element_by_css_selector('button[type=submit').click()
    credentials = True
except:
    print("error!! with your credentials, please restart the app and enter valid credentials")
    credentials = False

if(credentials == True):
    time.sleep(4)
    try:
        wrong_password = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[2]/p")
        if(len(wrong_password.text) > 0):
            print(wrong_password.text)
    except:
        time.sleep(2)
        try:
            driver.find_element_by_xpath('/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[1]/div/label/input')
            code = str(input("Enter authentication code: "))
            driver.find_element_by_xpath('/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[1]/div/label/input').send_keys(code)
            time.sleep(2)
            driver.find_element_by_css_selector('button[type=button').click()   
            print("Log in Successful...")
            logged_in = True
        except:
            print("Log in Successful...")
            logged_in = True
else:
    print("Closing App")

if(logged_in == True):
    time.sleep(4)
    try:
        driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/section/div/div[2]')
        driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button').click()
        print("Login info not saved...")
    except:
        print("Log info not saved by backend")

    try:
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[2]/div')
        driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        print("Notifications turned off!")
    except:
        print("Notifications turned off!")

    #opening main profile page
    main_page_url = "https://www.instagram.com/" + user_id
    driver.get(main_page_url)
    print("You are now on your profile page...")

    time.sleep(2)

    #accessing followers and following
    number_of_followers = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').text
    number_of_followings = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span').text

    print("Followers:")
    print(number_of_followers)
    print("Following:")
    print(number_of_followings)
    followers = int(input("Enter number of followers: "))
    followings = int(input("Enter number of followings: "))

    print("Loading information...Please be patient!")
    #accessing followers
    driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').click()
    time.sleep(2)
    fBody = driver.find_element_by_css_selector("div[class='isgrP']")
    scrolling_times = ((followers) // 5)
    scroll = 0
    scroll_count = scrolling_times 
    for scroll in tqdm(range(scroll_count), desc="Fetching Followers"):
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
        time.sleep(2)

    a_list = fBody.find_elements_by_tag_name('a')
    followers_list = []

    for i in tqdm(range(len(a_list)), desc="Updating your followers data"):
        if(len(a_list[i].get_attribute('title')) > 0):
            followers_list.append(a_list[i].get_attribute('title'))

    #accessing followings
    driver.get(main_page_url)

    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a').click()
    time.sleep(2)
    fBody = driver.find_element_by_css_selector("div[class='isgrP']")
    scrolling_times = ((followings) // 5)
    scroll = 0
    scroll_count = scrolling_times
    for scroll in tqdm(range(scroll_count), desc="Fetching Followings"):
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
        time.sleep(2)
    
    b_list = driver.find_elements_by_tag_name('a')
    followings_list = []

    for i in tqdm(range(len(b_list)), desc="Updating your followings data"):
        if(len(b_list[i].get_attribute('title')) > 0):
            followings_list.append(b_list[i].get_attribute('title'))

    print("Loaded Information Successfully!")
    #updating user info
    database_handler.updating_user_info(user_id, followers_list, followings_list)

    print("Analayze posts?")
    option = input()

    if(option == 'y' or option == 'Y'):
        no_of_posts = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span').text
        print("Total Posts: ")
        print(no_of_posts)
        print("Enter Number of Posts: ")
        no_posts = int(input())

        scrolling_times = ((no_posts) // 5)
        scroll = 0
        scroll_count = scrolling_times 

        links = set()
        for scroll in tqdm(range(scroll_count), desc="Analyzing Page"):
            box = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[3]/article')
            posts = box.find_elements_by_tag_name('a')
            for i in range(len(posts)):
                links.add(posts[i].get_attribute('href'))
            if(len(links) == no_posts):
                break
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        video_counts = 1
        display_likes = 0
        actual_likes = 0

        for link in links:
            driver.get(link)
            likers = set()

            time.sleep(2)
            try:
                likes = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div[2]/button/span').text
                display_likes += (int(likes.rstrip("%")))
                driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div[2]/button').click()
                #driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div/button').click()
                time.sleep(2)
                fBody = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/div')
                tbody = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/div/div')
                scrolling_times = (int(likes) // 5)
                scroll = 0
                scroll_count = scrolling_times 
                for scroll in tqdm(range(scroll_count), desc="Fetching Likers"):
                    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
                    time.sleep(2)
                    all_likers = tbody.find_elements_by_tag_name('a')
                    for i in range(len(all_likers)):
                        if(len(all_likers[i].get_attribute('title')) > 0):
                            likers.add(all_likers[i].get_attribute('title'))
        
                actual_likes += len(likers)
            except:
                print(f"Found {video_counts} video which is not being analyzed...")
                video_counts += 1
    else:
        print("Thanks for using this application")
        
else:
    print("Logged in fail!! Please try again with valid credentials")