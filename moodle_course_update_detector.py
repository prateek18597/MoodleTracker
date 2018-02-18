# moodle course update checker : automatically checks for updates in courses registered on moodle

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import getpass
import datetime
now = datetime.datetime.now()

# credentials for login
username = "cs160008j.iitju"

# read password from file
# f = open("password.txt","r")
# contents = f.read()
# password = contents
# f.close()
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.

# take password as input from terminal, it won't be visible
password = getpass.getpass("Password:")

# start a browser session
browser = webdriver.Chrome("/users/sahilbansal/Downloads/chromedriver", chrome_options=options) # change the parameter with the path of chromedriver

# open link in browser
browser.get('http://moodlej.iitjammu.ac.in/login/index.php')

# login
nameElem = browser.find_element_by_id('username')
nameElem.send_keys(username)

passElem = browser.find_element_by_id('password')
passElem.send_keys(password)

browser.find_element_by_id('loginbtn').click()

# computer architecture course
course = "http://moodlej.iitjammu.ac.in/course/view.php?id="
csl216_id = 33
csl216_link = course + str(csl216_id)

# open csl216 course
browser.get(csl216_link)

# get the current week day
f = open("current_week_day.txt","r")
current_day_of_week = int(f.read())
f.close()

# find previous time the script was run and the current day
f = open("prevDay.txt","r+")
prev_day = int(f.read())
current_day = now.day

# if script is being run for 1st time today, update the prevDay file with current day and increment the current week day
# needs to be run daily to maintain consistency in current week day
if(prev_day != current_day):
    current_day_of_week += 1
    f.seek(0)
    f.truncate()
    f.write(str(current_day))
f.close()

# update the current week day file
f = open("current_week_day.txt","w")
f.write(str(current_day_of_week))
f.close()

# get the appropriate section to check from file
f = open("sectionNo.txt","r+")
section_no = int(f.read())
# section no. updates when current_day_of_week = 8
if(current_day_of_week == 8):
    section_no += 1
    f.seek(0)
    f.truncate()
    f.write(str(section_no))
    f.close()
    # also need to update the current week day file with value 1
    f = open("current_week_day.txt","w")
    current_day_of_week = 1
    f.write(str(current_day_of_week))
    f.close()
    # also need to update the no. of links to 0 since new week started
    f = open("links.txt","w")
    f.write("0")
    f.close()

# checking for updates

section_id = "section-" + str(section_no)

# find the a tag whose parent is li with required section id
x_path_selector = "//li[@id='" + section_id + "']/*//a"
links = len(browser.find_elements(By.XPATH, x_path_selector))

# check whether count of links has increased, update if it has
f = open("links.txt","r+")
current_links = int(f.read())
if(current_links != links):
    f.seek(0)
    f.truncate()
    f.write(str(links))
    print("New material added in CSL216 course.")
f.close()
