#!/usr/bin/env python
# coding: utf-8

# Import necessary files
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.layouts import gridplot
from data_preparation import *

############################################
# *****    Define your parameters    ***** #
#                                          #
# Specify all combinations of parameters   #
# you want to compare using scatterplots.  #
#                                          #
# ---------------------------------------- #

# Define data to plot. Title is optional
plots = [
    {
        "title": "Compare number to average length",
        "x_axis": "20m_nof_comments",
        "y_axis": "20m_avg_len_comment"
    },
    {
        "title": "Compare number to median length",
        "x_axis": "20m_nof_comments",
        "y_axis": "20m_med_len_comment"
    },
    {
        "title": "Compare tonality to voting result",
        "x_axis": "tonality_mediareport",
        "y_axis": "voting_result"
    },
    {
        "title": "Compare amount of add prints to voting result",
        "x_axis": "nof_ads_print",
        "y_axis": "voting_result"
    },
    {
        "title": "Compare percentage of yes adds to voting result",
        "x_axis": "yes_ads",
        "y_axis": "voting_result"
    },
    {
        "title": "Compare amount of add prints to voting result",
        "x_axis": "nof_ads_print",
        "y_axis": "voting_result"
    },
    {
        "title": "Compare Topic to 20min comments",
        "x_axis": "topic_main",
        "y_axis": "20m_nof_comments"
    },
    {
        "title": "Compare Topic to voter turnout",
        "x_axis": "topic_main",
        "y_axis": "voter_turnout"
    },
    {
        "title": "Compare Topic to voting result",
        "x_axis": "topic_main",
        "y_axis": "voting_result"
    },
    {
        "title": "Compare voter turnout to voting result",
        "x_axis": "voter_turnout",
        "y_axis": "voting_result"
    },
]

# Define attribute for marker mapping
# Options:
#    - topic_markers    => Main topic of initiative
#    - pol_markers     => Political affilate that supported initiative
#    - verdict_markers  => vote accepted/rejected
use_marker = "topic_markers"

# Define attribute for color mapping
# Options:
#    - topic_color    => Main topic of initiative
#    - pol_colors     => Political affilate that supported initiative
#    - verdict_color  => vote accepted/rejected
use_color = "pol_colors"

# Define marker size and transparency
marker_size = 18
marker_alpha = 0.8

# ---------------------------------------- #
# ***  Hands off the following code!!  *** #
############################################

# Prepare data using separate python file
cds = collect_and_wash()

# Construct glyphs
glyphs = []
for plot in plots:
    # Visualize the data
    p = figure(width = 400, height=400, tools=plot_tools,
               title=(plot["title"] if "title" in plot else f"{plot['x_axis']} x {plot['y_axis']}"))
    p.scatter(source=cds, x=plot["x_axis"], y=plot["y_axis"], size=marker_size,
              color=use_color, line_color=None, alpha=marker_alpha, marker=use_marker)
    p.xaxis.axis_label = parameter_dict[plot["x_axis"]]
    p.yaxis.axis_label = parameter_dict[plot["y_axis"]]
    p.sizing_mode = "scale_both"
    
    # Add hover tool
    hover = HoverTool(tooltips=[
        ("Initiative", "@vote_title"),
        ("Topic", "@topic_label"),
        ("Affiliation", "@pol_desc"),
        (parameter_dict[plot["x_axis"]], "@" + plot["x_axis"]),
        (parameter_dict[plot["y_axis"]], "@" + plot["y_axis"])
    ])
    p.add_tools(hover)
    
    # Append glyph
    glyphs.append(p)

# make a grid and plot everything
output_file(filename="analysis-selective_comparison.html", title="SoComp - Group 1 - Multi-Compare")

grid = gridplot(glyphs, ncols=4, sizing_mode="stretch_both", merge_tools=False)
show(grid)