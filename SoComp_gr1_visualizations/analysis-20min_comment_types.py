#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, FactorRange
import datetime as dt
from math import pi
from bokeh.models import LabelSet
import bokeh.palettes as bp

# Read data into a dataframe using pandas
df = pd.read_csv('SoComp_clean_datasheet.csv')

# Convert "vote_nr" attribute to string
df['vote_nr'] = "V"+df['vote_nr'].astype(str)

verdicts = ["positive", "neutral", "negative"]
colors = ["#00ff00", "#cccccc", "#ff0000"]
data = {'comments': df['vote_nr'],
        'negative': df['20m_nof_comments_negative'],
        'neutral': df['20m_nof_comments_neutral'],
        'positive': df['20m_nof_comments_positive'],
        'Initiative': df['vote_title']
       }

source_stack = ColumnDataSource(data)

p = figure(x_range=df["vote_nr"], height=800, title="Number of comments in 20minuten")
p.vbar_stack(verdicts, x='comments', width=0.8, color=colors, source=source_stack,
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
    ("Comment type", "$name"),
    ("Number of comments", "@$name")
])
p.add_tools(hover)

output_file(filename="analysis-20min_comment_types.html", title="SoComp - Group 1")
show(p)