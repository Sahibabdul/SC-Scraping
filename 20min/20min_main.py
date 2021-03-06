from urllib import response
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from xml.dom import minidom 
import csv


#urls = ["https://www.20min.ch/story/bei-lex-netflix-wird-es-knapp-695939832762", "https://www.20min.ch/story/buergerliche-bekaempfen-stimmrechtsalter-16-mit-fake-statements-490546418948", "https://www.20min.ch/story/cervelat-werbeverbot-hat-keine-chance-485954729793", "https://www.20min.ch/story/darum-geht-es-bei-der-frontex-vorlage-486320411249", "https://www.20min.ch/story/gescheitertes-mediengesetz-gibt-erneuter-attacke-auf-srg-aufwind-741839757365", "https://www.20min.ch/story/aargauer-verleger-will-plakat-von-gegnern-verbieten-597445079291"]

vote_dict = {}

with open("SoComp - Datasheet.csv", "r", encoding="utf-8") as data_in:
    csv_reader = csv.reader(data_in, delimiter=",")
    line_count = 0

    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            vote_dict[row[1].replace("\n","").replace("\"", "")] = row[2].split("\n")
print(vote_dict)
for key in vote_dict.keys():
    for item in vote_dict[key]:
        if not "https://" in item:
            vote_dict[key] = vote_dict[key].remove(item)

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

def get_comments_from_url(url):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(r'C:\Users\PhilippMarock\Downloads\chromedriver_win32\chromedriver.exe', chrome_options=chrome_options)
    driver.get("https://www.20min.ch/comment/" + str(url.split("-")[-1]))
    driver.find_element_by_id("onetrust-accept-btn-handler").click()
    time.sleep(2)
    if not driver.title == "20 Minuten - Seite nicht gefunden":
        scroll_to_EOP(driver)
        time.sleep(2)
        comments = driver.find_element_by_id("commentSection").text
        driver.close()
        comments = comments.split("\n")[5:]
        print(len(comments))
        return comments
    else :
        return ""


for item in vote_dict.keys():
    urls = vote_dict[item]
    if urls is not None and len(urls) > 0:
        articles = {}
        xml_str = ""
        for url in urls:
            articles[url] = get_comments_from_url(url)
        for article in articles.keys():
            comments = articles[article]    
            comments = "\n".join(comments)
            comments = comments.replace("Werbung\n", "")
            comments = comments.split("Kommentar melden\n")
            comments = comments[:-1]
            root = minidom.Document()
            xml = root.createElement(article)
            root.appendChild(xml)
            print(article)
            for comment in comments:
                comment = comment.split("\n")[:-1]
                print(comment)
                print(article)

                try:
                    productChild = root.createElement("Comment")
                    productChild.setAttribute("author", comment[0])
                    productChild.setAttribute("creation_date", comment[1])
                    productChild.setAttribute("text", comment[2])
                    productChild.setAttribute("reactions", comment[3])
                    productChild.setAttribute("main_reaction", comment[4].split("(")[0])
                    if comment[-1] != "jetzt bewerten":
                        productChild.setAttribute("main_reaction_amount", comment[4].split("(")[1].replace(" Lesende)", ""))
                    else:
                        productChild.setAttribute("main_reaction_amount", "NA")
                    xml.appendChild(productChild)
                except:
                    print("------------------------")
                    print(comment)
                    print(article)
                    print("------------------------")
                
            xml_str = xml_str + root.toprettyxml(indent ="\t")
        xml_str = xml_str.replace("<?xml version=\"1.0\" ?>\n", "")
        with open(str(item)+".xml", "w", encoding="utf-8") as files:
            files.write(xml_str)