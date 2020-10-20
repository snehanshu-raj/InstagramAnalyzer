#C:\Users\Snehanshu Raj\Downloads\chromedriver_win32\chromedriver.exe

import database_handler
from selenium import webdriver
import requests
import time

chromePath = r"C:\Users\Snehanshu Raj\Downloads\chromedriver_win32\chromedriver.exe"

driver = webdriver.Chrome(executable_path=chromePath)

driver.get('https://www.instagram.com/accounts/login/')

#logging in
logged_in = False

time.sleep(2)
user_id = input("Enter username or phone number: ")
driver.find_element_by_xpath('/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div/div[1]/div/label/input').send_keys(user_id)

time.sleep(2)
password = input("Enter Password: ")
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

    #accessing followers and following
    number_of_followers = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span').text
    number_of_followings = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span').text

    print("Followers:")
    print(number_of_followers)
    print("Following:")
    print(number_of_followings)
    followers = int(input("Enter number of followers: "))
    followings = int(input("Enter number of followings: "))

    #accessing followers
    driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a').click()
    time.sleep(2)
    fBody = driver.find_element_by_css_selector("div[class='isgrP']")
    scrolling_times = ((followers) / 4)
    scroll = 0
    scroll_count = scrolling_times + 5  
    while scroll < scroll_count:
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
        time.sleep(2)
        scroll += 1
    
    a_list = driver.find_elements_by_tag_name('a')
    followers_list = []

    for f_name in a_list:
        if(len(f_name.get_attribute('title')) > 0):
            followers_list.append(f_name.get_attribute('title'))
    print(followers_list)

    #accessing followings
    driver.get(main_page_url)

    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[3]/a').click()
    time.sleep(2)
    fBody = driver.find_element_by_css_selector("div[class='isgrP']")
    scrolling_times = ((followings) / 4)
    scroll = 0
    scroll_count = scrolling_times + 5  
    while scroll < scroll_count:
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
        time.sleep(2)
        scroll += 1
    
    b_list = driver.find_elements_by_tag_name('a')
    followings_list = []

    for f_name in b_list:
        if(len(f_name.get_attribute('title')) > 0):
            followings_list.append(f_name.get_attribute('title'))
    print(followings_list)

    #updating user info
    database_handler.updating_user_info(user_id, followers_list, followings_list)

else:
    print("Logged in fail!! Please try again with valid credentials")