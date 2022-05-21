import csv

from germansentiment import SentimentModel
from textblob_de import TextBlobDE
import xml.etree.ElementTree as ET
import os


initiatives = []
for file in os.listdir('Analyzer/'):
    if file.endswith('.xml'):
        initiatives.append(file)

for file in initiatives:
    print(file)
    with open ("Analyzer/"+str(file), "r", encoding="utf-8") as file_in:
        lines = file_in.readlines()
    with open ("Analyzer/"+str(file), "w", encoding="utf-8") as file_out:
        for line in lines:
            file_out.write(str(line[:2]) + str(line[2:-4
            ].replace("/", "").replace(":","")) +str(line[-4:]))

for votes in initiatives:
    print(votes)
    tree = ET.parse('Analyzer/'+ str(votes))
    root = tree.getroot()

    model = SentimentModel()
    text = []

    # Blob-Analysis:

    for comment in root.findall('Comment'):
        dertext = comment.get('text')
        text.append(TextBlobDE(dertext))

    print("starting_blob")

    result_blob=[]
    for satz in text:
        result_blob.append(TextBlobDE(str(satz)).sentiment)
        print(result_blob[-1])


    with open('Analysis/'+str(votes)+'SoComp-Sentiment_Analysis_Blob.csv', 'w') as file:
        csv_file = csv.writer(file)
        for i in range(len(result_blob)):
            csv_file.writerow([str(text[i]), result_blob[i]])

