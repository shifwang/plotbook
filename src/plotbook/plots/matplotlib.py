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
    
def make_scatter_plot(Xs, Y, df, force_dtype={}, **params):
    fig, ax = plt.subplots(
        figsize=(params['Figsize_x'], params['Figsize_y'])
    )
    if isinstance(Xs, str):
        Xs = [Xs]
    if len(Xs) == 1:
        ax.scatter(df[Xs[0]], df[Y],
                   s=params['markersize'],
                   alpha=params['alpha'],
                   color=params['color'],
                    )
    elif len(Xs) == 2:
        values = sorted(df[Xs[0]].unique())
        for X1_unique in values:
            ordered = df[df[Xs[0]] == X1_unique]
            ax.scatter(ordered[Xs[1]], ordered[Y],
                s=params['markersize'],
                alpha=params['alpha'],
            )
        ax.legend(values)
    
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
        fig.savefig('saved_scatter_plot.png')

def make_interactive_scatter_plot(Xs, Y, df, force_dtype={}):
    def plot(**params):
        make_scatter_plot(Xs, Y, df, force_dtype, **params)
    key = Xs if isinstance(Xs, str) else Xs[1]
    widgets.interact(
        plot,
        Title="",
        xlabel=key,
        ylabel=Y,
        xmin=widgets.FloatSlider(
            min=df[key].min() - (df[key].max() - df[key].min())/10,
            max=df[key].min(),
            value=df[key].min() - (df[key].max() - df[key].min())/20,
            step=max(df[key].max() - df[key].min(),1)/100,
        ),
        xmax=widgets.FloatSlider(
            min=df[key].max(),
            max=df[key].max() + (df[key].max() - df[key].min())/10,
            value=df[key].max() + (df[key].max() - df[key].min())/20,
            step=(df[key].max() - df[key].min())/100,
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
        color=[
            ('steelblue','steelblue'),
            ('blue','b'),
            ('green','g'),
            ('red','r'),
            ('cyan','c'),
            ('magenta','m'),
            ('yellow','y'),
            ('black','k'),
            ('white','w'),
        ],
        alpha=widgets.FloatSlider(
            min=0,
            max=1,
            value=1,
            step=0.01,
        ),
        half_spine=True,
        save=False,
    )
def make_line_plot(Xs, Y, df, force_dtype={}, **params):
    fig, ax = plt.subplots(
        figsize=(params['Figsize_x'], params['Figsize_y'])
    )
    if isinstance(Xs, str):
        Xs = [Xs]
    if len(Xs) == 1:
        ordered = df.sort_values(Xs[0])
        ax.plot(ordered[Xs[0]], ordered[Y],
                   marker=params['marker'],
                   markersize=params['markersize'],
                   linewidth=params['linewidth'],
                   color=params['color'],
                  )
    elif len(Xs) == 2:
        values = sorted(df[Xs[0]].unique())
        for X1_unique in values:
            ordered = df[df[Xs[0]] == X1_unique].sort_values(Xs[1])
            ax.plot(
                ordered[Xs[1]],
                ordered[Y],
                markersize=params['markersize'],
                linewidth=params['linewidth'],
            )
        ax.legend(values)
    else:
        raise NotImplementedError()
                         
                         
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
        fig.savefig('saved_line_plot.png')

def make_interactive_line_plot(Xs, Y, df, force_dtype={}):
    def plot(**params):
        make_line_plot(Xs, Y, df, force_dtype, **params)
    key = Xs if isinstance(Xs, str) else Xs[1]
    widgets.interact(
        plot,
        Title="",
        xlabel=key,
        ylabel=Y,
        xmin=widgets.FloatSlider(
            min=df[key].min() - (df[key].max() - df[key].min())/10,
            max=df[key].min(),
            value=df[key].min() - (df[key].max() - df[key].min())/20,
            step=max(df[key].max() - df[key].min(),1)/100,
        ),
        xmax=widgets.FloatSlider(
            min=df[key].max(),
            max=df[key].max() + (df[key].max() - df[key].min())/10,
            value=df[key].max() + (df[key].max() - df[key].min())/20,
            step=(df[key].max() - df[key].min())/100,
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
        marker=[('Point', '.'), ('Square', "s"), ("circle", 'o'), ('star', '*')],
        markersize=widgets.IntSlider(
            min=1,
            max=100,
            value=10,
            step=1,
        ),
        linewidth=widgets.FloatSlider(
            min=0.5,
            max=10,
            value=2,
            step=0.5,
        ),
        color=[
            ('steelblue','steelblue'),
            ('blue','b'),
            ('green','g'),
            ('red','r'),
            ('cyan','c'),
            ('magenta','m'),
            ('yellow','y'),
            ('black','k'),
            ('white','w'),
        ],
        half_spine=True,
        save=False,
    )

def make_pie_chart(X, Y, df, force_dtype={}, **params):
    fig, ax = plt.subplots()
    if 'shadow' not in params:
        params['shadow'] = True
    if 'startangle' not in params:
        params['startangle'] = startangle
    ax.pie(
        df[Y],
        labels=df[X],
        autopct='%1.1f%%',
        shadow=params['shadow'],
        startangle=params['startangle'],
    )
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show(fig)


def make_violin_plot(X, Y, df, force_dtype={}, **params):
    pass

def make_box_plot(X, Y, df, force_dtype={}, **params):
    pass