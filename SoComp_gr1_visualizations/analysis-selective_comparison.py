#!/usr/bin/env python
# coding: utf-8

# Import necessary files
import pandas as pd
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import gridplot
import bokeh.palettes as bp
import datetime as dt

############################################
# *****    Define your parameters    ***** #
#                                          #
# Specify all combinations of parameters   #
# you want to compare using scatterplots.  #
#                                          #
# ---------------------------------------- #
plots = [
    {
        "title": "Compare number to average length",
        "x_axis": "20m_nof_comments",
        "y_axis": "20m_avg_len_comment",
        "x_axis_label": "Number of comments in 20min",
        "y_axis_label": "Average length of comments"
    },
    {
        "title": "Compare number to median length",
        "x_axis": "20m_nof_comments",
        "y_axis": "20m_med_len_comment",
        "x_axis_label": "Number of comments in 20min",
        "y_axis_label": "Median length of comments"
    },
    {
        "title": "Compare tonality to voting result",
        "x_axis": "tonality_mediareport",
        "y_axis": "voting_result",
        "x_axis_label": "Tonality in Medienberichterstattungen",
        "y_axis_label": "Result of Vote (in percent)"
    },
]

# ---------------------------------------- #
# ***  Hands off the following code!!  *** #
############################################


# Read data into a dataframe using pandas
df = pd.read_csv('SoComp_clean_datasheet.csv')

# ***********  Clean the data  *********** #

# Convert "vote_nr" attribute to string
df['vote_nr'] = "V" + df['vote_nr'].astype(str)

# Assign collors to main topic
topic_colors = bp.Set3[max(df['topic_main'])]
df['topic_color'] = df['topic_main'].apply(lambda topic: topic_colors[topic - 1])

# Convert "voting_date" to datetime type
df['voting_date'] = pd.to_datetime(df['voting_date'], infer_datetime_format=True)

# Assign collors and descriptions to political affiliation
# Source: https://medium.com/srf-schweizer-radio-und-fernsehen/wie-wir-bei-srf-parteien-einfärben-9f010f80cf62
pol_desc = ["Partei-übergreifend/parteilos", "Grüne, SP", "EVP", "Mitte, GLP", "FDP", "SVP"]
pol_colors = ["#cccccc", "#ff0000", "#ff8700", "#beef00", "#063cff", "#009a2e"]
df['pol_desc'] = df['political_affiliation'].apply(lambda aff: pol_desc[aff])
df['pol_colors'] = df['political_affiliation'].apply(lambda aff: pol_colors[aff])

# Convert "voter_turnout" attribute to float
df['voter_turnout'] = df['voter_turnout'].str.rstrip('%').astype('float')

# Convert "voting_result" attribute to float
df['voting_result'] = df['voting_result'].str.rstrip('%').astype('float')

# Convert "staendemehr" attribute to float
df['staendemehr'] = df['staendemehr'].str.rstrip('%').astype('float')

# Convert "yes_ads" attribute to float
df['yes_ads'] = df['yes_ads'].str.rstrip('%').astype('float')

# Assign collors to verdict
verdict_colors = {"YES": "#2ca02c", "NO": "#d62728"}
df['verdict_color'] = df['verdict'].apply(lambda v: verdict_colors[v])

# ***********  Washing complete  *********** #

# Convert dataframe to ColumnDataSource
cds = ColumnDataSource(df)

glyphs = []
for plot in plots:
    # Visualize the data
    p = figure(width=400, height=400, title=plot["title"])
    p.scatter(source=cds, x=plot["x_axis"], y=plot["y_axis"], size=15, color="pol_colors")
    p.xaxis.axis_label = plot["x_axis_label"]
    p.yaxis.axis_label = plot["y_axis_label"]
    p.sizing_mode = "scale_both"
    
    # Add hover tool
    hover = HoverTool(tooltips=[
        ("Initiative", "@vote_title"),
        ("Political affiliation", "@pol_desc"),
        (plot["x_axis_label"], "@" + plot["x_axis"]),
        (plot["y_axis_label"], "@" + plot["y_axis"])
    ])
    p.add_tools(hover)
    
    # Append glyph
    glyphs.append(p)

# make a grid and plot everything
output_file(filename="analysis-selective_comparison.html", title="SoComp - Group 1 - Multi-Compare")

grid = gridplot(glyphs, ncols=3, sizing_mode="stretch_both")
show(grid)