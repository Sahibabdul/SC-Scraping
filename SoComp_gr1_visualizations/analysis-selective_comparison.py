#!/usr/bin/env python
# coding: utf-8

# Import necessary files
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.layouts import gridplot
from data_preparation import parameter_dict, collect_and_wash

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
]


# ---------------------------------------- #
# ***  Hands off the following code!!  *** #
############################################

# Prepare data using separate python file
cds = collect_and_wash()

# Construct glyphs
glyphs = []
for plot in plots:
    # Visualize the data
    p = figure(width = 400, height=400,
               title=(plot["title"] if "title" in plot else f"{plot['x_axis']} x {plot['y_axis']}"))
    p.scatter(source=cds, x=plot["x_axis"], y=plot["y_axis"], size=20,
              color="pol_colors", line_color=None, alpha=1, marker="verdict_markers")
    p.xaxis.axis_label = parameter_dict[plot["x_axis"]]
    p.yaxis.axis_label = parameter_dict[plot["y_axis"]]
    p.sizing_mode = "scale_both"
    
    # Add hover tool
    hover = HoverTool(tooltips=[
        ("Initiative", "@vote_title"),
        ("Political affiliation", "@pol_desc"),
        (parameter_dict[plot["x_axis"]], "@" + plot["x_axis"]),
        (parameter_dict[plot["y_axis"]], "@" + plot["y_axis"])
    ])
    p.add_tools(hover)
    
    # Append glyph
    glyphs.append(p)

# make a grid and plot everything
output_file(filename="analysis-selective_comparison.html", title="SoComp - Group 1 - Multi-Compare")

grid = gridplot(glyphs, ncols=4, sizing_mode="stretch_both")
show(grid)