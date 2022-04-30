from urllib import response
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(r'C:\Users\PhilippMarock\Downloads\chromedriver_win32\chromedriver.exe', chrome_options=chrome_options)

url = "https://www.20min.ch/story/bei-lex-netflix-wird-es-knapp-695939832762"
driver.get(url)

driver.find_element_by_id("onetrust-accept-btn-handler").click()

element = driver.find_element_by_class_name("CommentArea_loadMoreComment__itQ7e")
action = ActionChains(driver)
action.move_to_element(element).perform()
driver.find_element_by_class_name("CommentArea_loadMoreCommentButton__GRJxx").click()

time.sleep(1)
cur_url = driver.current_url
driver.close()

print(cur_url)
req_response = urlopen(cur_url)
html_bytes = req_response.read()
html_string = html_bytes.decode("utf-8")

soup = BeautifulSoup(html_string, features="html.parser")
comments = soup.find_all('p', class_ = "CommentCard_body__KWmXR")

print(comments)
