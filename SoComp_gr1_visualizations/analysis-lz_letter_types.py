#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, FactorRange

# Read data into a dataframe using pandas
df = pd.read_csv('SoComp_clean_datasheet.csv')

# Convert "vote_nr" attribute to string
df['vote_nr'] = "V"+df['vote_nr'].astype(str)

verdicts = ["positive", "neutral", "negative"]
colors = ["#00ff00", "#cccccc", "#ff0000"]
data = {'letters': df['vote_nr'],
        'negative': df['lz_opinion_neg'],
        'neutral': df['lz_opinion_neutral'],
        'positive': df['lz_opinion_pos'],
        'Initiative': df['vote_title']
       }

source_stack = ColumnDataSource(data)

p = figure(x_range=df["vote_nr"], height=800, title="Number of reader's letters in Luzerner Zeitung")
p.vbar_stack(verdicts, x='letters', width=0.8, color=colors, source=source_stack,
             legend_label=verdicts)

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_right"
p.legend.orientation = "horizontal"
p.sizing_mode = "stretch_width"

# Add hover tool
hover = HoverTool(tooltips = [
    ("Initiative", "@Initiative"),
    ("Opinion", "$name"),
    ("Number of reader's letters", "@$name")
])
p.add_tools(hover)

output_file(filename="analysis-lz_letter_types.html", title="SoComp - Group 1 - LZ letter types")
show(p)