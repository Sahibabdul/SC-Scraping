import csv

from germansentiment import SentimentModel
from textblob_de import TextBlobDE
import xml.etree.ElementTree as ET
import os
import statistics
import re


initiatives = []
for file in os.listdir('Comments20min/'):
    if file.endswith('.xml'):
        initiatives.append(file)

'''
for file in initiatives:
    print(file)
    with open ("Comments20min/"+str(file), "r", encoding="utf-8") as file_in:
        lines = file_in.readlines()
    with open ("Comments20min/"+str(file), "w", encoding="utf-8") as file_out:
        for line in lines:
            file_out.write(str(line[:2]) + str(line[2:-4
            ].replace("/", "").replace(":","")) +str(line[-4
            :])) 
'''

print(initiatives)

for votes in initiatives:
    print(votes)
    tree = ET.parse('Comments20min/'+ str(votes))
    root = tree.getroot()

    model = SentimentModel()

    text = []
    reactions = {}
    main_reactions_amount = {}
    reactions_amount = {}
    sentiment = {}
    authors = []
    len_comments = []
    num_reactions_postive = 0
    num_reactions_negative = 0
    num_reactions_neutral = 0
    total_reactions = 0
    tendency_positive = 0
    tendency_negative = 0
    tendency_neutral = 0
    #Bert-Analysis:

    for comment in root.findall('Comment'):
        buffer = comment.get('text').replace(",","").replace(";","")
        text.append(buffer)
        len_comments.append(len(buffer))
        authors.append(comment.get("author"))
        reactions[buffer] = comment.get("main_reaction")
        if comment.get("main_reaction_amount") == "NA":
            main_reactions_amount[buffer] = 0
        else:
            main_reactions_amount[buffer] = comment.get("main_reaction_amount")
        reactions_amount[buffer] = comment.get("reactions")
        buffer = comment.get("reactions")
        if buffer == "NA":
            total_reactions += 0
        else:
            total_reactions += int(buffer)

    sentiment_res = {}
    for x in range(len(text)):
        sentiment_res[text[x]] = model.predict_sentiment([text[x]])
        print(sentiment_res[text[x]])
        print(reactions[text[x]])
        if sentiment_res[text[x]] == ['negative']:
            num_reactions_negative += int(reactions_amount[text[x]])
            if reactions[text[x]] in ["SO NICHT", "QUATSCH", "UNNÖTIG"]:
                tendency_negative -= int(re.search(r'\d+', reactions_amount[text[x]]).group())
            elif reactions[text[x]] in ["SMART", "GENAU", "LOVE IT"]:
                tendency_negative += int(re.search(r'\d+', reactions_amount[text[x]]).group())
        elif sentiment_res[text[x]] == ['positive']:
            num_reactions_postive += int(re.search(r'\d+', reactions_amount[text[x]]).group())
            if reactions[text[x]] in ["SO NICHT", "QUATSCH", "UNNÖTIG"]:
                tendency_positive -= int(re.search(r'\d+', reactions_amount[text[x]]).group())
            elif reactions[text[x]] in ["SMART", "GENAU", "LOVE IT"]:
                tendency_positive += int(re.search(r'\d+', reactions_amount[text[x]]).group())
        elif sentiment_res[text[x]] == ['neutral']:
            num_reactions_neutral += int(re.search(r'\d+', reactions_amount[text[x]]).group())
            if reactions[text[x]] in ["SO NICHT", "QUATSCH", "UNNÖTIG"]:
                tendency_neutral -= int(re.search(r'\d+', reactions_amount[text[x]]).group())
            elif reactions[text[x]] in ["SMART", "GENAU", "LOVE IT"]:
                tendency_neutral += int(re.search(r'\d+', reactions_amount[text[x]]).group())
        else:
            print("problem with sentiment counting")

        
        print(str(x)+"/"+str(len(text)))


    with open('Comments20min/'+str(votes)+'SoComp-Analysis.csv', 'w') as file:
        csv_file = csv.writer(file)
        csv_file.writerow(["Nof commentators", "Average Comments/commentators", "Average length of comment (in words)", "Median length of comment (in words)", "Nof comments positive", "Nof comments neutral", "Nof comments negative", "Tendency to positive comments (all main_reactions +/- added together and then divided by total reactions)", "# Reactions to positive comments", "Tendency to neutral comments (all main_reactions +/- added together and then divided by total reactions)", "# Reactions to neutral comments", "Tendency to negative comments (all main_reactions +/- added together and then divided by total reactions)", "# Reactions to negative comments"])
        num_of_commentators = authors
        num_of_commentators = len(list(dict.fromkeys(num_of_commentators)))
        aver_comment_per_auth = len(text) / num_of_commentators
        aver_len_comment = int(sum(len_comments)) / int(len(len_comments))
        median_len_comment = statistics.median(len_comments)
        
        num_positive_comments = 0
        num_negative_comments = 0
        num_neutral_comments = 0

        for sen in sentiment_res.values():
            if sen == ['negative']:
                num_negative_comments += 1
            elif sen == ['positive']:
                num_positive_comments += 1
            elif sen == ['neutral']:
                num_neutral_comments += 1
            else:
                print("problem with sentiment counting")

        csv_file.writerow([str(num_of_commentators), str(aver_comment_per_auth), str(aver_len_comment), str(median_len_comment), str(num_positive_comments), str(num_negative_comments), str(num_neutral_comments), str(tendency_positive/total_reactions), str(num_reactions_postive), str(tendency_neutral/total_reactions), str(num_reactions_neutral),  str(tendency_negative/total_reactions), str(num_reactions_negative)])

        csv_file.writerow(["Text","Sentiment", "main reaction", "main reaction amount", "all reactions"])
        for i in range(len(text)):
            csv_file.writerow([str(text[i]), sentiment_res[text[i]], reactions[text[i]], main_reactions_amount[text[i]], reactions_amount[text[i]]])