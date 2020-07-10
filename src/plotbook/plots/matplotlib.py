import pandas as pd
import matplotlib.pyplot as plt
import ipywidgets as widgets
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
    return heatmap(x, y, counts)
    
def make_scatter_plot(X, Y, df, force_dtype={}, **params):
    fig, ax = plt.subplots(
        figsize=(params['Figsize_x'], params['Figsize_y'])
    )
    ax.scatter(df[X], df[Y],
               s=params['markersize'],
               alpha=params['alpha'])
    ax.set_xlabel(params['xlabel'])
    ax.set_ylabel(params['ylabel'])
    if 'Title' in params:
        ax.set_title(params['Title'])
    if 'xmin' in params:
        ax.set_xlim(left=params['xmin'])
    if 'xmax' in params:
        ax.set_xlim(right=params['xmax'])
    if 'ymin' in params:
        ax.set_ylim(bottom=params['ymin'])
    if 'ymax' in params:
        ax.set_ylim(top=params['ymax'])
    if 'half_spine' in params:
        ax.spines["top"].set_visible(not params['half_spine'])  
        ax.spines["right"].set_visible(not params['half_spine'])
    plt.show(fig)
    if params['save']:
        fig.savefig('saved.png')

def make_interactive_scatter_plot(X, Y, df, force_dtype={}):
    def plot(**params):
        make_scatter_plot(X, Y, df, force_dtype, **params)
    widgets.interact(
        plot,
        Title="",
        xlabel=X,
        ylabel=Y,
        xmin=widgets.FloatSlider(
            min=df[X].min() - (df[X].max() - df[X].min())/10,
            max=df[X].min(),
            value=df[X].min() - (df[X].max() - df[X].min())/20,
            step=max(df[X].max() - df[X].min(),1)/100,
        ),
        xmax=widgets.FloatSlider(
            min=df[X].max(),
            max=df[X].max() + (df[X].max() - df[X].min())/10,
            value=df[X].max() + (df[X].max() - df[X].min())/20,
            step=(df[X].max() - df[X].min())/100,
        ),
        ymin=widgets.FloatSlider(
            min=df[Y].min() - (df[Y].max() - df[Y].min())/10,
            max=df[Y].min(),
            value=df[Y].min()-(df[Y].max() - df[Y].min())/20,
            step=(df[Y].max() - df[Y].min())/100,
        ),
        ymax=widgets.FloatSlider(
            min=df[Y].max(),
            max=df[Y].max() + (df[Y].max() - df[Y].min())/10,
            value=df[Y].max()+(df[Y].max() - df[Y].min())/20,
            step=(df[Y].max() - df[Y].min())/100,
        ),
        Figsize_x=widgets.IntSlider(
            min=1,
            max=10,
            value=4,
        ),
        Figsize_y=widgets.IntSlider(
            min=1,
            max=10,
            value=3,
        ),
        markersize=widgets.IntSlider(
            min=1,
            max=100,
            value=10,
            step=1,
        ),
        alpha=widgets.FloatSlider(
            min=0,
            max=1,
            value=1,
            step=0.01,
        ),
        half_spine=True,
        save=False,
    )
def make_line_plot(X, Y, df, force_dtype={}, **params):
    fig, ax = plt.subplots()
    ordered = df.sort_values(X)
    ax.plot(ordered[X], ordered[Y], linewidth=2)
    ax.set_xlabel(X)
    ax.set_ylabel(Y)
    if 'title' in params:
        ax.set_title(params['title'])
    plt.show(fig)

def make_interactive_line_plot(X, Y, df, force_dtype={}):
    widgets.interact(
        lambda Title: make_line_plot(X, Y, df, force_dtype, title=Title),
        Title="Title",
    )