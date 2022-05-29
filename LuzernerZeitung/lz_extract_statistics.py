#!/usr/bin/env python
# coding: utf-8

import os
import csv
import statistics
import secrets

source_dir = "cpi_split-author_wrong/"
out_filename = "cpi_split-author_wrong/lz_statistics.csv"
file_prefix = "comments_"
file_suffix = ".csv"

# Correction factors
corr_factors = {
    "lz_nof_letters": 2.08,
    "lz_nof_writers": 2.02,
    "lz_avg_len_letter": 0.47,
    "lz_med_len_letter": 0.64,
    "lz_avg_opinion": 0.48
}
do_correction = True

# Select files to read
initiatives = []
for file in os.listdir(source_dir):
    if file.startswith(file_prefix):
        initiatives.append(file)
initiatives.sort()
# Collect information
lz_statistics = []
for initiative in initiatives:
    
    # Loop through csv files
    in_filename = source_dir + initiative
    rows = []
    with open(in_filename, "r", encoding="utf-8") as csv_file:
    
        # Init statistics
        len_letters = []
        authors = []
        opinions = []
        # We assign the following values to analysed type of comment
        opinion_values = {
            "positive": 1,
            "neutral": 0,
            "negative": -1
        }
        opinion_sums = {
            "positive": 0,
            "neutral": 0,
            "negative": 0
        }


        # Read file into array and collect information
        # The csv has 3 columns:
        #   0: text
        #   1: author
        #   2: analysis
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            rows.append(row)
            len_letters.append(len(row[0].strip().split(" ")))
            # If no author is provided, generate random string for correct counting
            authors.append(row[1] if row[1] else secrets.token_hex(5))
            # analysis = one of [positive, neutral, negative]
            # => We count the value of it
            analysis = row[2].strip("[]'")
            if analysis in opinion_values:
                opinions.append(opinion_values[analysis])
                opinion_sums[analysis] += 1
        
        # Ok, collection is done. Now for some statistics...
        if len(rows):
            lz_nof_letters = len(rows)
            lz_nof_writers = len(list(dict.fromkeys(authors)))
            lz_avg_len_letter = statistics.mean(len_letters)
            lz_med_len_letter = statistics.median(len_letters)
            lz_avg_opinion = statistics.mean(opinions)
            lz_opinion_pos = opinion_sums["positive"]
            lz_opinion_neutral = opinion_sums["neutral"]
            lz_opinion_neg = opinion_sums["negative"]
            if do_correction:
                lz_nof_letters = round(lz_nof_letters * corr_factors["lz_nof_letters"])
                lz_nof_writers = round(lz_nof_writers * corr_factors["lz_nof_writers"])
                lz_avg_len_letter *= corr_factors["lz_avg_len_letter"]
                lz_med_len_letter *= corr_factors["lz_med_len_letter"]
                lz_avg_opinion *= corr_factors["lz_avg_opinion"]
                lz_opinion_pos = round(lz_opinion_pos * corr_factors["lz_nof_letters"])
                lz_opinion_neutral = round(lz_opinion_neutral * corr_factors["lz_nof_letters"])
                lz_opinion_neg = round(lz_opinion_neg * corr_factors["lz_nof_letters"])
            lz_avg_letters_writer = lz_nof_letters / lz_nof_writers if lz_nof_writers else 0
        else:
            # Skip empty files
            lz_nof_letters = 0
            lz_nof_writers = 0
            lz_avg_letters_writer = 0
            lz_avg_len_letter = 0
            lz_med_len_letter = 0
            lz_avg_opinion = 0
            lz_opinion_pos = 0
            lz_opinion_neutral = 0
            lz_opinion_neg = 0

        # Append result row to statistics
        lz_statistics.append([
            initiative.lstrip(file_prefix).rstrip(file_suffix),
            lz_nof_letters,
            lz_nof_writers,
            lz_avg_letters_writer,
            lz_avg_len_letter,
            lz_med_len_letter,
            lz_avg_opinion,
            lz_opinion_pos,
            lz_opinion_neutral,
            lz_opinion_neg
        ])

# We have read everything into the array "lz_statistics".
# Now it's time to create the csv file

with open(out_filename, 'w') as file:
    csv_file = csv.writer(file)
    csv_file.writerow([
        "initiative",
        "lz_nof_letters",
        "lz_nof_writers",
        "lz_avg_letters_writer",
        "lz_avg_len_letter",
        "lz_med_len_letter",
        "lz_avg_opinion",
        "lz_opinion_pos",
        "lz_opinion_neutral",
        "lz_opinion_neg"
    ])
    for row in lz_statistics:
        csv_file.writerow(row)
