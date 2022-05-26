import pandas as pd
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, FactorRange


# Read data into a dataframe using pandas
df = pd.read_csv('SoComp_clean_datasheet.csv')

# Convert dataframe to ColumnDataSource
cds = ColumnDataSource(df)

# Visualize the data
p = figure(height=800, title="Comparison: 20minuten, number of comments - median length")

p.scatter(source=cds, x='20m_nof_comments', y='20m_med_len_comment', size=20)

p.xaxis.axis_label = "Number of comments in 20min"
p.yaxis.axis_label = "Median length of comments"
p.sizing_mode = "stretch_both"

# Add hover tool
hover = HoverTool(tooltips = [
    ("Number of comments", "@20m_nof_comments"),
    ("Median length (words)", "@20m_med_len_comment")
])
p.add_tools(hover)

# Show plot
output_file("analysis-comp-nof_comments-vs-med_len.html")
show(p)