import time

import selenium.common.exceptions
from selenium.webdriver import Chrome
from PIL import Image
import cv2
import pytesseract


def Start():
    global driver
    path = ''  # Enter the path to the chromedriver file
    driver = Chrome('/Users/vanshbhatia/Downloads/chromedriver')
    driver.maximize_window()
    driver.get("https://hostellogin.srmist.edu.in/srmclb/")
    info_enter()


def element_exists(element):
    try:
        driver.find_element_by_css_selector(element)
    except selenium.common.exceptions.NoSuchElementException:
        return False
    return True


def info_enter():
    uname = driver.find_element_by_css_selector('#accountname')
    pwd = driver.find_element_by_css_selector('#password')
    uname.send_keys('')#Enter your username
    pwd.send_keys('')#enter your password
    driver.save_screenshot('screenshot1.png')
    im = Image.open('screenshot1.png')
    iml = im.crop((2140, 890, 2305, 950))
    # iml.show()
    iml.save('captcha1.png')
    img = cv2.imread('captcha1.png')
    print(pytesseract.image_to_string(img))
    captcha_text = driver.find_element_by_css_selector('#capth')
    captcha_text.send_keys(pytesseract.image_to_string(img))
    submit = driver.find_element_by_css_selector(
        '#loginform1 > table > tbody > tr:nth-child(6) > td > input:nth-child(1)')
    submit.click()
    if element_exists('#loginform1 > table > tbody > tr:nth-child(1) > td > h4 > font'):

        if (driver.find_element_by_css_selector(
                '#loginform1 > table > tbody > tr:nth-child(1) > td > h4 > font').text == 'Enter valid Captcha.'):
            print('Wrong captcha, trying again')
            driver.refresh()
            info_enter()

        if (driver.find_element_by_css_selector(
                '#loginform1 > table > tbody > tr:nth-child(1) > td > h4 > font').text == 'Hostel booking is not Applicable'):
            print('Either credentials are wrong or it is Not open yet, trying in 10 mins')

            time.sleep(600)
            driver.refresh()
            info_enter()

        if (driver.find_element_by_css_selector(
                '#loginform1 > table > tbody > tr:nth-child(1) > td > h4 > font').text == 'Service yet to start'):
            print('Service yet to start, trying in 20s')
            time.sleep(20)
            driver.refresh()
            info_enter()
    print('_______________________________________________________\nLogged In Successfully 😇\n\n')
    print("If you want to retry login (Close the browser and try again), press 1\nTo quit with the browser window "
          "open, press 2 \nTo Quit entirely, press any other key (BROWSER WINDOW WILL BE CLOSED)")
    usr_inp = input()
    if usr_inp == '1':
        driver.close()
        Start()
    elif usr_inp == '2':
        quit(0)
    else:
        driver.close()


Start()
