# scratch.py
from bashplotlib.scatterplot import plot_scatter

x_coords = [-10,20,30]
y_coords = [-10,20,30]
width = 10
char = 'x'
color = 'default'
title = 'My Test Graph'
ytitle = 'My Y title'
xtitle = 'My X title'

plot_scatter(
    None,
    x_coords,
    y_coords,
    width,
    char,
    color,
    title,
    ytitle=ytitle,
    xtitle=xtitle
)