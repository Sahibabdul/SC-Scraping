#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, FactorRange
import datetime as dt
from math import pi
from bokeh.models import LabelSet
from bokeh.palettes import Category20, Set3
from bokeh.layouts import column, row, gridplot

# Read data into a dataframe using pandas
df = pd.read_csv('SoComp_clean_datasheet.csv')

# Convert "voting_date" attribute in the dataframe to datetime type for further processing
df['voting_date'] = pd.to_datetime(df['voting_date'])

# Convert "voter_turnout" attribute to float
df['voter_turnout'] = df['voter_turnout'].str.rstrip('%').astype('float')

# Convert "vote_nr" attribute to string
df['vote_nr'] = "V"+df['vote_nr'].astype(str)

# Assign collors to main topic
topic_colors = Set3[max(df['topic_main'])]
df['topic_color'] = df['topic_main'].apply(lambda topic: topic_colors[topic-1])


# Convert dataframe to ColumnDataSource
cds = ColumnDataSource(df)


# Visualize the data using bokeh plot functions
p = figure(x_range=cds.data["vote_nr"], plot_width=800, y_range=(0, 80),
           title='Voter turnout per initiative')

p.xaxis.axis_label = "Initiative"
p.yaxis.axis_label = "voter turnout in %"
p.xgrid.grid_line_color = None
p.x_range.range_padding = 0
p.sizing_mode = "stretch_width"

# Add hover tool
hover = HoverTool(tooltips = [
    ("Vote Nr", "@vote_nr"),
    ("Initiative", "@vote_title"),
    ("Main Topic", "@topic_main"),
    ("Topics", "@topic_text"),
    ("Turnout", "@voter_turnout")
])
p.add_tools(hover)

p.vbar(source=cds, x='vote_nr', bottom=0, top='voter_turnout', width=0.5, color='topic_color')

# Save the plot output_file
output_file(filename="analysis-all_turnouts.html", title="SoComp - Group 1")
show(p)