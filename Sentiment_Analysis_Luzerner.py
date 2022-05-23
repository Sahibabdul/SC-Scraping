import csv
from germansentiment import SentimentModel
import xml.etree.ElementTree as ET


with open ("LuzernerZeitung/comments.xml", "r", encoding="utf-8") as file_in:
        lines = file_in.readlines()

tree = ET.parse("LuzernerZeitung/comments.xml")
root = tree.getroot()

model = SentimentModel()

text = []

#Bert-Analysis:

for comment in root.findall("comment"):
    buffertext = comment.get('text')
    text.append(buffertext)

result = []
for comment in range(len(text)):
    result.append(model.predict_sentiment([text[comment]]))
    print(str(comment)+"/"+str(len(text))+str(result[-1]))
print(result)



with open("LuzernerZeitung/comments.xml"+ "SoComp-Analysis.csv", 'w') as file:
    csv_file = csv.writer(file)
    for i in range(len(result)):
        csv_file.writerow([str(text[i]), result[i]])