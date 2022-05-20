import csv

from germansentiment import SentimentModel
from textblob_de import TextBlobDE
import xml.etree.ElementTree as ET
import os


initiatives = []
for file in os.listdir('Comments20min/'):
    if file.endswith('.xml'):
        initiatives.append(file)

for file in initiatives:
    print(file)
    with open ("Comments20min/"+str(file), "r", encoding="utf-8") as file_in:
        lines = file_in.readlines()
    with open ("Comments20min/"+str(file), "w", encoding="utf-8") as file_out:
        for line in lines:
            file_out.write(str(line[:2]) + str(line[2:-4
            ].replace("/", "").replace(":","")) +str(line[-4
            :])) 

for votes in initiatives:
    print(votes)
    tree = ET.parse('Comments20min/'+ str(votes))
    root = tree.getroot()

    model = SentimentModel()

    text = []

    #Bert-Analysis:

    for comment in root.findall('Comment'):
        dertext = comment.get('text')
        text.append(dertext)

    print("starting1")
    result = []
    for comment in range(len(text)):
        result.append(model.predict_sentiment([text[comment]]))
        print(str(comment)+"/"+str(len(text))+str(result[-1]))
    print(result)

    #Blob-Analysis:
    result_blob=[]
    for satz in text:
        result_blob.append("yikes")#TextBlobDE(satz).sentiment)


    with open('Comments20min/'+str(votes)+'SoComp-Analysis.csv', 'w') as file:
        csv_file = csv.writer(file)
        for i in range(len(result)):
            csv_file.writerow([str(text[i]), result[i]])