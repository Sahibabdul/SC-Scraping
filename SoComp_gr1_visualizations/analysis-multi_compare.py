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
# All parameters will be compared with     #
# each other in (n 2) scatterplots.        #
#                                          #
# ---------------------------------------- #
params = [
    "20m_nof_comments",
    "20m_avg_len_comment",
    "20m_med_len_comment",
    "20m_nof_comments_positive",
    "20m_nof_comments_neutral",
    "20m_nof_comments_negative",
    "20m_tendency_positive",
    "20min_reactions_positive",
    "20m_tendency_neutral",
    "20min_reactions_neutral",
    "20m_tendency_negative",
    "20min_reactions_negative"
]
# ---------------------------------------- #
# ***  Hands off the following code!!  *** #
############################################

# Prepare data using separate python file
cds = collect_and_wash()

glyphs = []
for px in range(len(params)):
    for py in range(px, len(params)):
    
        # We don't have to compare values to themselves
        if px == py:
            continue
    
        # Visualize the data
        p = figure(width=400, height=400, title=f"{params[px]} x {params[py]}")
        p.scatter(source=cds, x=params[px], y=params[py], size=20,
                  color="pol_colors",  line_color=None, alpha=1, marker="verdict_markers")
        p.xaxis.axis_label = parameter_dict[params[px]]
        p.yaxis.axis_label = parameter_dict[params[py]]
        p.sizing_mode = "scale_both"
        
        # Add hover tool
        hover = HoverTool(tooltips=[
            ("Initiative", "@vote_title"),
            ("Political affiliation", "@pol_desc"),
            (parameter_dict[params[px]], f"@{params[px]}"),
            (parameter_dict[params[py]], f"@{params[py]}")
        ])
        p.add_tools(hover)
        
        # Append glyph
        glyphs.append(p)

# make a grid and plot everything
output_file(filename="analysis-multi_compare.html", title="SoComp - Group 1 - Multi-Compare")

grid = gridplot(glyphs, ncols=4, sizing_mode="stretch_both")
show(grid)