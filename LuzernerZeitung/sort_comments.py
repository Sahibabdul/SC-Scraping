import csv

file_name = "comments.xmlSoComp-Analysis.csv"
rows = []
with open(file_name, "r", encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        rows.append(row)

words = ["initiative", "abstimmung", "gesetz", "kampfflugzeug", "kinderdrittbetreuungskosten", "begrenzungsinitiative", "zuwanderung", "kriegsmaterial", "verhüllungsverbot", " ehe ", "covid", "corona", "pflegeinitiative", "transplantationsgesetz", "filmgesetz"]

out = []
with open("onlyInitiative_jz.csv", "w", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    for row in rows:
        if any(sub_str in row[0].lower() for sub_str in words):
            out.append([row[0], row[1]])
    writer.writerows(out)