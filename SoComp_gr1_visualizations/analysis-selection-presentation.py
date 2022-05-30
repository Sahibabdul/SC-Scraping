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
# Specify all combinations of parameters   #
# you want to compare using scatterplots.  #
#                                          #
# ---------------------------------------- #

"""
    voter_turnout
    voting_result
    nof_ads_print
    yes_ads
    nof_mediareport
    tonality_mediareport
    lz_nof_letters
    lz_nof_writers
    lz_avg_letters_writer
    lz_avg_len_letter
    lz_med_len_letter
    lz_avg_opinion
    20m_nof_arcitles
    20m_nof_comments
    20m_avg_comments_article
    20m_nof_commentators
    20m_avg_comments_commentator
    20m_avg_len_comment
    20m_med_len_comment
    20m_nof_comments_positive
    20m_nof_comments_neutral
    20m_nof_comments_negative
    20m_tendency_positive
    20min_reactions_positive
    20m_tendency_neutral
    20min_reactions_neutral
    20m_tendency_negative
    20min_reactions_negative

"""

# Define data to plot. Title is optional
plots = [
    {
        "title": "Compare ads to number of reader's letters",
        "x_axis": "nof_ads_print",
        "y_axis": "lz_nof_letters"
    },
    {
        "title": "Compare voter turnout to number of writers",
        "x_axis": "voter_turnout",
        "y_axis": "lz_nof_writers"
    },
    {
        "title": "Compare voter turnout to 20min commentators",
        "x_axis": "voter_turnout",
        "y_axis": "20m_nof_commentators",
        "use_color": "pol_colors"
    },
    {
        "title": "Compare 'YES' ads to tonality in media reports",
        "x_axis": "yes_ads",
        "y_axis": "tonality_mediareport"
    },
    {
        "title": "Compare tonality in media reports to voting result",
        "x_axis": "tonality_mediareport",
        "y_axis": "voting_result",
        "use_color": "pol_colors"
    },
    {
        "title": "No correlation between average lengths",
        "x_axis": "lz_avg_len_letter",
        "y_axis": "20m_avg_len_comment"
    },
    {
        "title": "Compare 'YES' ads to tonality in media reports",
        "x_axis": "yes_ads",
        "y_axis": "tonality_mediareport",
        "use_color": "pol_colors"
    },
    {
        "title": "Compare topic to reader's letters, parties and outcome",
        "x_axis": "topic_main",
        "y_axis": "lz_nof_letters",
        "use_marker": "verdict_markers",
        "use_color": "pol_colors"
    },
    {
        "title": "Compare topic to comments, parties and outcome",
        "x_axis": "topic_main",
        "y_axis": "20m_nof_comments",
        "use_marker": "verdict_markers",
        "use_color": "pol_colors"
    },
]

# Define attribute for marker mapping
# Options:
#    - topic_markers    => Main topic of initiative
#    - pol_markers     => Political affilate that supported initiative
#    - verdict_markers  => vote accepted/rejected
default_marker = "topic_markers"

# Define attribute for color mapping
# Options:
#    - topic_color    => Main topic of initiative
#    - pol_colors     => Political affilate that supported initiative
#    - verdict_color  => vote accepted/rejected
default_color = "verdict_color"

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
    # Overwrite default marker and color if specified
    use_marker = plot["use_marker"] if "use_marker" in plot else default_marker
    use_color = plot["use_color"] if "use_color" in plot else default_color
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
output_file(filename="analysis-selection-presentation.html", title="SoComp - Group 1 - Multi-Compare")
grid = gridplot(glyphs, ncols=3, sizing_mode="stretch_both", merge_tools=False)
title = Div(text="""<h1>Relation between Reader’s Letters, Online Comments & Voting Outcomes.</h1>""",
            height=100)
show(column([title, grid],
            sizing_mode="stretch_both",
        ))
#show(grid)