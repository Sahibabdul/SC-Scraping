from urllib.request import urlopen
from html.parser import HTMLParser
from urllib import parse
from bs4 import BeautifulSoup
import logging

class Leserbrief:
    url = "https://www.volksblatt.li/Leserbriefe/"


    def __init__(self, id):
        self.id=str(id)
        self.url = Leserbrief.url+self.id
        self.title="body_hTitel"
        self.creator="body_divInfo"
        self.text="body_divText"

        response = urlopen(self.url)
        if 'text/html' in response.getheader('Content-Type'):
            html_bytes = response.read()
            html_string = html_bytes.decode("utf-8")
        if "Dieser Artikel ist nicht verfügbar" in html_string:
            self.text="Error"
            return

        soup = BeautifulSoup(html_string, features="html.parser")
        self.title = str(soup.find("h1", {"id": self.title}))
        self.creator = str(soup.find("div", {"id": self.creator}))
        self.text = str(soup.find("div", {"id": self.text}))
        self.title = self.remove_tags(self.title)
        self.creator = self.remove_tags(self.creator)
        self.text = self.remove_tags(self.text)
        buffer_text = self.text.split()
        buffer_creator =self.creator.split()
        try:
            for i in range(len(buffer_text)):
                if buffer_text[i] == buffer_creator[1] and buffer_text[i+1] == buffer_creator[2]:
                    self.text=" ".join(self.text.split()[:i-1])
                    break
        except IndexError as reee:
            self.text="Error"
        
        
                
    def get_title(self):
        return self.title
    

    def get_text(self):
        return self.text


    def get_creator(self):
        return self.creator


    def remove_tags(self, text_str):
        buffer = text_str.replace("<div class=\"text\" id=\"body_divText\"><p>"," ")
        buffer = buffer.replace("<div id=\"body_divInfo\">"," ")
        buffer = buffer.replace("<p>"," ")
        buffer = buffer.replace("</p>"," ")
        buffer = buffer.replace("<br/>"," ")
        buffer = buffer.replace("</div>"," ")
        buffer = buffer.replace("<h1 id=\"body_hTitel\">"," ")
        return buffer.replace("</h1>"," ")


    def __str__(self):
        return self.text