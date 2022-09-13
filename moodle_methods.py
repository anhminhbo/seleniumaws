import sys
import datetime
import moodle_locators as locators
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1400,1500")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")


driver = webdriver.Chrome(options=options)


# Fixture method - to open web browser
def setUp():
    # Make a full screen
    driver.maximize_window()

    # Let's wait for the browser response in general
    driver.implicitly_wait(30)

    # Navigating to the Moodle app website
    driver.get('https://www.google.com/')

    # Checking that we're on the correct URL address and we're seeing correct title
    if driver.title == 'Google':
        print(f'We\'re at Moodle homepage -- {driver.current_url}')
        print(f'We\'re seeing title message -- "Software Quality Assurance Testing"')
    else:
        print(f'We\'re not at the Moodle homepage. Check your code!')
        driver.close()
        driver.quit()


# Fixture method - to close web browser
def tearDown():
    if driver is not None:
        print(f'--------------------------------------')
        print(f'Test Completed at: {datetime.datetime.now()}')
        driver.close()
        driver.quit()
        # Make a log file with dynamic fake values
        old_instance = sys.stdout
        log_file = open('message.log', 'w')
        sys.stdout = log_file
        print(f'Email: {locators.email}\nUsername: {locators.new_username}\nPassword: {locators.new_password}\n'
              f'Full Name: {locators.full_name}')
        sys.stdout = old_instance
        log_file.close()


# Log In method with custom (dynamic) username and password
def log_in(username, password):
    if driver.current_url == locators.moodle_url:
        driver.find_element(By.LINK_TEXT, 'Log in').click()
        if driver.current_url == locators.moodle_login_url:
            driver.find_element(By.ID, 'username').send_keys(username)
            sleep(0.25)
            driver.find_element(By.ID, 'password').send_keys(password)
            sleep(0.25)
            driver.find_element(By.ID, 'loginbtn').click()
            if driver.title == 'Dashboard' and driver.current_url == locators.moodle_dashboard_url:
                assert driver.current_url == locators.moodle_dashboard_url
                print(f'Log in successfully. Dashboard is present. \n'
                      f'We logged in with Username: {username} and Password: {password}')
            else:
                print(f'We\re not at the Dashboard. Try again')


# Log out method to log out from the Moodle app
def log_out():
    driver.find_element(By.CLASS_NAME, 'userpicture').click()
    sleep(0.25)
    driver.find_element(By.XPATH, '//span[contains(., "Log out")]').click()
    sleep(0.25)
    if driver.current_url == locators.moodle_url:
        print(f'Log out successfully at: {datetime.datetime.now()}')


# # Check if text Database connection error appear
# def checkDatabase():
    
