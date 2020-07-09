import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn

def heatmap(x, y, size):
    '''
    https://towardsdatascience.com/better-heatmaps-and-correlation-matrix-plots-in-python-41445d0f2bec
    '''
    plt.figure()
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

def make_occur_map(X, Y, df, force_dtype={}):
    output = df.apply(lambda row: (row[X], row[Y]), axis=1)
    values, counts = np.unique(output, return_counts=True)
    x = pd.Series([value[0] for value in values])
    y = pd.Series([value[1] for value in values])
    heatmap(x, y, counts)

def make_occur_map_2(X, Y, df, force_dtype={}):
    output = df.apply(lambda row: (row[X], row[Y]), axis=1)
    values, counts = np.unique(output, return_counts=True)
    x = pd.Series([value[0] for value in values])
    y = pd.Series([value[1] for value in values])
    
    x_labels = [v for v in sorted(x.unique())]
    y_labels = [v for v in sorted(y.unique())]
    x_to_num = {p[1]:p[0] for p in enumerate(x_labels)}
    y_to_num = {p[1]:p[0] for p in enumerate(y_labels)}
    out = pd.DataFrame(columns=x_labels, index=y_labels)
    for i, (x_ind, y_ind) in enumerate(zip(x, y)):
        out.loc[y_ind, x_ind] = counts[i]
    out = out.fillna(0)
    plt.figure()
    sn.heatmap(out)
