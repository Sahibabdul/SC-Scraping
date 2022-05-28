#!/usr/bin/env python
# coding: utf-8

import os
import csv

source_dir = "comments_per_initiative/"
dest_dir = "cpi_split-author/"

initiatives = []
for file in os.listdir(source_dir):
    if file.startswith("comments_V"):
        initiatives.append(file)

# Split authors, if possible

for initiative in initiatives:
    
    in_filename = source_dir + initiative
    out_filename = dest_dir + initiative

    rows = []
    with open(in_filename, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            rows.append(row)
    
    out = []
    with open(out_filename, "w", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        for row in rows:
            split_text = row[0].rsplit(".", 1)
            out.append([split_text[0]+".", split_text[1].lstrip(), row[1]])
        writer.writerows(out)
    
