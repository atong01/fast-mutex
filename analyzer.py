import csv
import numpy as np
import plotly
from plotly.offline import plot
import plotly.graph_objs as go

def make_trace(fname):
    csvfile = open(fname)
    creader = csv.reader(csvfile)
    data = []
    for row in creader:
        data.append(row)

    data = np.array(data[1:], dtype=np.float) # cut first and last lines

    trace = plotly.graph_objs.Scatter(
        x = data[:,0],
        y = data[:,3],
        mode = 'markers',
        name = fname
    )
    return trace

def make_plot(fnames, out_filename = 'results.html'):
    layout = dict(title = 'RMR per Crit vs. Contention',
                  yaxis = dict(title = 'RMR per Crit'),
                  xaxis = dict(title = 'Contention'))
    fig = go.Figure(data = list(map(make_trace, fnames)), layout = layout)
    plot(fig, filename=out_filename)

fnames = ['resultsrr.csv',]
make_plot(fnames)
