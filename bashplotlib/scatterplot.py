#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plotting terminal based scatterplots
"""

from __future__ import print_function
import csv
import sys
import optparse
from .utils.helpers import *
from .utils.commandhelp import scatter


def get_scale(series, is_y=False, steps=20):
    min_val = min(series)
    max_val = max(series)
    scaled_series = []
    for x in drange(min_val, max_val, (max_val - min_val) / steps,
                    include_stop=True):
        if x > 0 and scaled_series and max(scaled_series) < 0:
            scaled_series.append(0.0)
        scaled_series.append(x)

    if is_y:
        scaled_series.reverse()
    return scaled_series


def _plot_scatter(xs, ys, size, pch, colour, title, cs, xtitle, ytitle):
    plotted = set()
    x_scale = get_scale(xs, False, size)
    y_scale = get_scale(ys, True, size)
    scaled_length_x = len(x_scale)

    if title:
        print(box_text(title, 2 * (scaled_length_x + 1)))

    if ytitle:
        print(f"y: {ytitle}")

    print("+" + "-" * (2 * (scaled_length_x + 1)) + "+")
    yaxis = min(x_scale, key=abs) if min(x_scale) < 0 < max(x_scale) else None
    xaxis = min(y_scale, key=abs) if min(y_scale) < 0 < max(y_scale) else None
    for y in y_scale:
        print("|", end=' ')
        for x in x_scale:
            if x == xaxis and y == xaxis:
                point = "o"
            elif x == yaxis:
                point = "|"
            elif y == xaxis:
                point = "–"
            else:
                point = " "
            for (i, (xp, yp)) in enumerate(zip(xs, ys)):
                if xp <= x and yp >= y and (xp, yp) not in plotted:
                    point = pch
                    plotted.add((xp, yp))
                    if cs:
                        colour = cs[i]
            printcolour(point + " ", True, colour)
        print(" |")
    print("+" + "-" * (2 * (scaled_length_x + 1)) + "+")

    if xtitle:
        print("{0:>{1}}".format(f"x: {xtitle}", 2 * (scaled_length_x + 2)))

def plot_scatter(f, xs, ys, size, pch, colour, title, xtitle="", ytitle=""):
    """
    Form a complex number.

    Arguments:
        f -- comma delimited file w/ x,y coordinates
        xs -- if f not specified this is a file w/ x coordinates
        ys -- if f not specified this is a filew / y coordinates
        size -- size of the plot
        pch -- shape of the points (any character)
        colour -- colour of the points
        title -- title of the plot
    """
    cs = None
    if f:
        if isinstance(f, str):
            with open(f) as fh:
                data = [tuple(line.strip().split(',')) for line in fh]
        else:
            data = [tuple(line.strip().split(',')) for line in f]
        xs = [float(i[0]) for i in data]
        ys = [float(i[1]) for i in data]
        if len(data[0]) > 2:
            cs = [i[2].strip() for i in data]
    elif isinstance(xs, list) and isinstance(ys, list):
        pass
    else:
        with open(xs) as fh:
            xs = [float(str(row).strip()) for row in fh]
        with open(ys) as fh:
            ys = [float(str(row).strip()) for row in fh]

    _plot_scatter(xs, ys, size, pch, colour, title, cs, xtitle, ytitle)
    


def main():

    parser = optparse.OptionParser(usage=scatter['usage'])

    parser.add_option('-f', '--file', help='a csv w/ x and y coordinates', default=None, dest='f')
    parser.add_option('-t', '--title', help='title for the chart', default="", dest='t')
    parser.add_option('-X', '--xtitle', help='x-axis title', default="", dest='xtitle')
    parser.add_option('-Y', '--ytitle', help='y-ayis title', default="", dest='ytitle')
    parser.add_option('-x', help='x coordinates', default=None, dest='x')
    parser.add_option('-y', help='y coordinates', default=None, dest='y')
    parser.add_option('-s', '--size', help='y coordinates', default=20, dest='size', type='int')
    parser.add_option('-p', '--pch', help='shape of point', default="x", dest='pch')
    parser.add_option('-c', '--colour', help='colour of the plot (%s)' %
                      colour_help, default='default', dest='colour')

    opts, args = parser.parse_args()

    if opts.f is None and (opts.x is None or opts.y is None):
        opts.f = sys.stdin.readlines()

    if opts.f or (opts.x and opts.y):
        plot_scatter(opts.f, opts.x, opts.y, opts.size, opts.pch, opts.colour, opts.t, opts.xtitle, opts.ytitle)
    else:
        print("nothing to plot!")


if __name__ == "__main__":
    main()
