import csv

# Define keywords
words_per_initiative = {
    "V01": ["radiogebühr", "fernsehgebühr", "billag", "bilag", "srf", "serafe"],
    "V02": ["fairfood", "fair-food", "lebensmittel", "umweltfreundlich"],
    "V03": ["sozialversicherungsrecht", "atsg", "überwachung", "versicherte"],
    "V04": ["siedlungsentwicklung", "zersiedelung"],
    "V05": ["kampfflugzeug", "kampflugzeug", "gripen", "kriegsflugzeug", "militär"],
    "V06": ["bundessteuer", "kinderbetreuungskosten", "kinderdrittbetreuungskosten", "kinderabzug"],
    "V07": ["zuwanderung", "begrenzungsinitiative", "einwanderung"],
    "V08": ["kriegsmaterial", "rüstungsfirma", "rüstungsfirmen"],
    "V09": ["konzernverantwortung", "unternehmen"],
    "V10": ["verhüllungsverbot", "burka", "kopftuch", "kopftücher", "muslim"],
    "V11": ["co2", "treibhausgas", "emissionen", "flugticket"],
    "V12": ["ehe ", "homosexuell", "heirat", "hochzeit"],
    "V13": ["99 ", "99-", "kapital", "bonus", "boni", "abfindung"],
    "V14": ["covid", "corona", "pandemie", "berset"],
    "V15": ["pflege", "pflegeinitiative", "transplantationsgesetz"],
    "V16": ["frontex", "küstenwache", "grenzwache"],
    "V17": ["transplantation", "organ", "patientenverfügung"],
    "V18": ["filmgesetz", "netflix"]
}
generic_keywords = ["initiative", "abstimmung", "gesetz"]

# Create combined list with all keywords
all_keywords = generic_keywords
for kw in words_per_initiative.values():
    all_keywords += kw

# Read analysis file into array
csv_rows = []
#file_name = "onlyInitiative.csv"
# with open(file_name, "r", encoding="utf-8", newline ='\r\n') as csv_file:
file_name = "comments.xmlSoComp-Analysis.csv"
with open(file_name, "r", encoding="utf-8", newline ='\n') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        csv_rows.append(row)

# Init counters and collectors
match = 0
counters = {}
letter_collections = {}
for key in words_per_initiative:
    counters[key] = 0
    letter_collections[key] = []
counters["no_category_found"] = 0
counters["skipped"] = 0
letter_collections["no_category_found"] = []
letter_collections["skipped"] = []

# Scan data
print("Scanning for keywords...")
for row in csv_rows:
    # if no keyword is found - even no generic one => ignore letter
    if not any(sub_str in row[0].lower() for sub_str in all_keywords):
        letter_collections["skipped"].append(row)
        counters["skipped"] += 1
        continue

    found_category = False
    for initiative, keywords in words_per_initiative.items():
        if any(sub_str in row[0].lower() for sub_str in keywords):
            letter_collections[initiative].append(row)
            counters[initiative] += 1
            found_category = True
            #out.append([row[0], row[1]])
    if found_category:
        match += 1
    else:
        letter_collections["no_category_found"].append(row)
        counters["no_category_found"] += 1

# Write to files data
print("Writing csv files...")
for initiative, letters in letter_collections.items():
    out_filename = "comments_" + initiative + ".csv"
    with open("comments_per_initiative/" + out_filename, "w", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(letters)

print (f"Found {match} of total {len(csv_rows)} letters with keywords.")
print (f"{counters['skipped']} letters did not even contain a generic keyword and were skipped")
for initiative, letters in letter_collections.items():
    print(f"{initiative}: {len(letters)}")
