import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def heatmap(x, y, size):
    '''
    https://towardsdatascience.com/better-heatmaps-and-correlation-matrix-plots-in-python-41445d0f2bec
    '''
    fig, ax = plt.subplots()

    # Mapping from column names to integer coordinates
    x_labels = [v for v in sorted(x.unique())]
    y_labels = [v for v in sorted(y.unique())]
    x_to_num = {p[1]:p[0] for p in enumerate(x_labels)}
    y_to_num = {p[1]:p[0] for p in enumerate(y_labels)}

    size_scale = 500
    ax.scatter(
        x=x.map(x_to_num), # Use mapping for x
        y=y.map(y_to_num), # Use mapping for y
        s=size * size_scale, # Vector of square sizes, proportional to size parameter
        marker='s' # Use square as scatterplot marker
    )
    margin = 0.5
    ax.set_xlim([- margin, len(x_labels) - 1 + margin])
    ax.set_ylim([- margin, len(y_labels) - 1 + margin])
    

    # Show column labels on the axes
    ax.set_xticks([x_to_num[v] for v in x_labels])
    ax.set_xticklabels(x_labels, rotation=45, horizontalalignment='right')
    ax.set_yticks([y_to_num[v] for v in y_labels])
    ax.set_yticklabels(y_labels)
    plt.show(fig)

def make_occur_plot(X, Y, df, force_dtype={}):
    output = df.apply(lambda row: (row[X], row[Y]), axis=1)
    values, counts = np.unique(output, return_counts=True)
    x = pd.Series([value[0] for value in values])
    y = pd.Series([value[1] for value in values])
    heatmap(x, y, counts)
    
def make_scatter_plot(X, Y, df, force_dtype={}):
    fig, ax = plt.subplots()
    ax.scatter(df[X], df[Y])
    plt.show(fig)

def make_line_plot(X, Y, df, force_dtype={}):
    fig, ax = plt.subplots()
    ordered = df.sort_values(X)
    ax.plot(ordered[X], ordered[Y], linewidth=2)
    plt.show(fig)
