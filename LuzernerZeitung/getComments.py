from urllib import response
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from xml.dom import minidom 
import csv


with open("LuzernerZeitung/links.txt", "r", encoding="utf-8") as data_in:
    lines = data_in.readlines()

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(r'C:\Users\PhilippMarock\Downloads\chromedriver_win32\chromedriver.exe', chrome_options=chrome_options)
root = minidom.Document()
xml = root.createElement("Articles")
root.appendChild(xml)
for link in lines:
    try:    
        driver.get(link)
        title = driver.find_element_by_class_name("headline__title").text
        subtitle = driver.find_element_by_class_name("headline__lead").text
        buffer = driver.find_elements_by_class_name("text")
        text=""
        for i in buffer:
            text += i.text
        productChild = root.createElement(link)
        productChild.setAttribute("title", title)
        productChild.setAttribute("subtitle", subtitle)
        productChild.setAttribute("text", text)
        xml.appendChild(productChild)
    except:
        pass
xml_str = root.toprettyxml(indent ="\t")
xml_str = xml_str.replace("<?xml version=\"1.0\" ?>\n", "")
with open("LuzernerZeitung/comments.xml", "w", encoding="utf-8") as files:
    files.write(xml_str)