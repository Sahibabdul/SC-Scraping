#!/usr/bin/env python
# coding: utf-8

# Import necessary files
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.layouts import gridplot, column
from data_preparation import *
from bokeh.models import Div

############################################
# *****    Define your parameters    ***** #
#                                          #
# All parameters will be compared with     #
# each other in (n 2) scatterplots.        #
#                                          #
# ---------------------------------------- #
params = [
    "voter_turnout",
    "voting_result",
    "nof_ads_print",
    "yes_ads",
    "nof_mediareport",
    "tonality_mediareport",
    "lz_nof_letters",
    "lz_nof_writers",
    "lz_avg_letters_writer",
    "lz_avg_len_letter",
    "lz_med_len_letter",
    "lz_avg_opinion",
    "20m_nof_arcitles",
    "20m_nof_comments",
    "20m_avg_comments_article",
    "20m_nof_commentators",
    "20m_avg_comments_commentator",
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

# Specify output title and filename
out_title = "SoComp - Group 1 - Full-Comparison, Colors = Political affilates"
out_filename = "analysis-full_comparison-pol_colors"
title = Div(text="""<h1>SoComp - Group 1 – Full-Comparison, Colors = Political affilates</h1>""",
            height=100)

#out_title = "SoComp - Group 1 - Full-Comparison, Colors = Verdicts"
#out_filename = "analysis-full_comparison-verdict_color"
#title = Div(text="""<h1>SoComp - Group 1 – Full-Comparison, Colors = Verdicts</h1>""",
#            height=100)

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
        p = figure(width=400, height=400, tools=plot_tools, title=f"{params[px]} x {params[py]}")
        p.scatter(source=cds, x=params[px], y=params[py], size=marker_size,
                  color=use_color,  line_color=None, alpha=marker_alpha, marker=use_marker)
        p.xaxis.axis_label = parameter_dict[params[px]]
        p.yaxis.axis_label = parameter_dict[params[py]]
        p.sizing_mode = "scale_both"
        
        # Add hover tool
        hover = HoverTool(tooltips=[
            ("Initiative", "@vote_title"),
            ("Topic", "@topic_label"),
            ("Affiliation", "@pol_desc"),
            (parameter_dict[params[px]], f"@{params[px]}"),
            (parameter_dict[params[py]], f"@{params[py]}")
        ])
        p.add_tools(hover)
        
        # Append glyph
        glyphs.append(p)

# make a grid and plot everything

html_filename = out_filename + ".html"
png_filename = out_filename + ".png"

output_file(filename=html_filename, title=out_title)

grid = gridplot(glyphs, ncols=4, sizing_mode="stretch_both", merge_tools=False)

show(column([title, grid],
            sizing_mode="stretch_both",
        ))
#show(grid)