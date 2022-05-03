from urllib import response
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from xml.dom import minidom 


urls = ["https://www.20min.ch/story/bei-lex-netflix-wird-es-knapp-695939832762", "https://www.20min.ch/story/buergerliche-bekaempfen-stimmrechtsalter-16-mit-fake-statements-490546418948", "https://www.20min.ch/story/cervelat-werbeverbot-hat-keine-chance-485954729793"]

def scroll_to_EOP(driver):
    SCROLL_PAUSE_TIME = 0.5

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

def get_comments_from_url(url):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(r'C:\Users\PhilippMarock\Downloads\chromedriver_win32\chromedriver.exe', chrome_options=chrome_options)
    driver.get("https://www.20min.ch/comment/" + str(url.split("-")[-1]))
    driver.find_element_by_id("onetrust-accept-btn-handler").click()
    scroll_to_EOP(driver)
    comments = driver.find_element_by_id("commentSection").text
    time.sleep(2)
    driver.close()
    comments = comments.split("\n")[5:]
    print(len(comments))
    return comments

with open("comments_20min.xml", "w", encoding="utf-8") as writer:
    comments = get_comments_from_url(urls[0])
    comments = "\n".join(comments)
    comments = comments.split("Kommentar melden\n")
    comments = comments[:-1]
    root = minidom.Document()
    xml = root.createElement("Netflix")
    root.appendChild(xml)
    for comment in comments:
        comment = comment.split("\n")
        print(comment)
        productChild = root.createElement("Comment")
        productChild.setAttribute("author", comment[0])
        productChild.setAttribute("creation_date", comment[1])
        productChild.setAttribute("text", comment[2])
        productChild.setAttribute("reactions", comment[3])
        productChild.setAttribute("main_reaction", comment[4].split("(")[0])
        productChild.setAttribute("main_reaction_amount", comment[4].split("(")[0].replace(" Lesende)", ""))
        xml.appendChild(productChild)
    xml_str = root.toprettyxml(indent ="\t") 
    with open("comments_20min.xml", "w", encoding="utf-8") as files:
        files.write(xml_str)