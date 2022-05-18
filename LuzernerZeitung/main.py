from urllib import response
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from xml.dom import minidom 
import csv

url ="https://www.luzernerzeitung.ch/meinung/leserbriefe"

def scroll_to_EOP(driver):
    SCROLL_PAUSE_TIME = 1.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


last = 0
cur =  0

def write2file(links):

    with open("LuzernerZeitung/links.txt", "w", encoding="utf-8") as data_out:
        for link in buffer:            
            data_out.write(str(link.get_attribute('href'))+"\n")

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(r'C:\Users\PhilippMarock\Downloads\chromedriver_win32\chromedriver.exe', chrome_options=chrome_options)

driver.get(url)

links = []
buffer = driver.find_elements_by_class_name("teaser__link")
flag = True
time.sleep(2)
while flag:
    scroll_to_EOP(driver)
    element = driver.find_element_by_class_name("button--loadmore")
    print(element)
    print("...........")
    actions = ActionChains(driver)
    actions.move_to_element(element).click().perform()
    flag = True
    time.sleep(0.5)
    if element is None:
        flag = False
    
    print(flag)
    last = len(buffer)
    buffer = driver.find_elements_by_class_name("teaser__link")
    buffer = list(dict.fromkeys(buffer))
    write2file(buffer)
    print("Writing to file: " + str(last) + " / " + str(cur))