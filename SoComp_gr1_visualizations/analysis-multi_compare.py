import pandas as pd
from bokeh.io import output_file, show, save
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, FactorRange
from bokeh.layouts import gridplot

# Read data into a dataframe using pandas
df = pd.read_csv('SoComp_clean_datasheet.csv')

# Convert dataframe to ColumnDataSource
cds = ColumnDataSource(df)

# Define parameters to compare
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

glyphs = []
for px in range(len(params)):
    for py in range(px, len(params)):
    
        # We don't have to compare values to themselves
        if px == py:
            continue
    
        # Visualize the data
        p = figure(width=400, height=400, title=f"{params[px]} x {params[py]}")
        p.scatter(source=cds, x=params[px], y=params[py], size=15)
        p.xaxis.axis_label = params[px]
        p.yaxis.axis_label = params[py]
        p.sizing_mode = "scale_both"
        
        # Add hover tool
        hover = HoverTool(tooltips=[
            (params[px], f"@{params[px]}"),
            (params[py], f"@{params[py]}")
        ])
        p.add_tools(hover)
        
        # Add glyph to record
        glyphs.append(p)

# make a grid and plot everything
output_file(filename="analysis-multi_compare.html", title="SoComp - Group 1 - Multi-Compare")

grid = gridplot(glyphs, ncols=4, sizing_mode="stretch_both")
show(grid)