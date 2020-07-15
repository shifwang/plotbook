import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
import ipywidgets as widgets


def make_occur_plot_2(X, Y, df, force_dtype={}):
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
    #plt.figure()
    ax = sn.heatmap(out)
    fig = ax.get_figure()
    plt.show(fig)
    

def make_beeswarm_plot(Xs, Y, df, force_dtype={}, **params):
    plt.figure(figsize=(params['Figsize_x'], params['Figsize_y']))
    if params['color_palette'] == '':
        with sn.color_palette():
            if isinstance(Xs, str):
                ax = sn.swarmplot(x=Xs, y = Y, data=df)
            else:
                ax = sn.swarmplot(x=Xs[1], y = Y, data=df,hue=Xs[0])
    else:
        key = Xs if isinstance(Xs, str) else Xs[0]
        with sn.color_palette(params['color_palette'], df[key].nunique()):
            if isinstance(Xs, str):
                ax = sn.swarmplot(x=Xs, y = Y, data=df)
            else:
                ax = sn.swarmplot(x=Xs[1], y = Y, data=df,hue=Xs[0])
    ax.set_title(params['Title'])
    if 'half_spine' in params:
        ax.spines["top"].set_visible(not params['half_spine'])  
        ax.spines["right"].set_visible(not params['half_spine'])
    ax.set_xlabel(params['xlabel'])
    ax.set_ylabel(params['ylabel'])
    fig = ax.get_figure()
    plt.show(ax)
    if params['save']:
        fig.savefig('saved_beeswarm_plot.png')

def make_interactive_beeswarm(Xs, Y, df, force_dtype={}):
    def plot(**params):
        make_beeswarm_plot(Xs, Y, df, force_dtype, **params)
    if isinstance(Xs, str):
        widgets.interact(
            plot,
            Title="",
            xlabel=Xs,
            ylabel=Y,
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
            color_palette=[
                ('default',''),
                ('muted','muted'),
                ('Red-Blue','RdBu'),
                ('Set1','Set1'),
                ('Set2','Set2'),
                ('Set3','Set3'),
                ('husl','husl'),
                ('spring', 'spring'),
                ('summer', 'summer'),
                ('ocean', 'ocean'),
            ],
            half_spine=True,
            save=False,
        )
    elif len(Xs) == 2:
        widgets.interact(
            plot,
            Title="",
            xlabel=Xs[1],
            ylabel=Y,
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
            color_palette=[
                ('default',''),
                ('muted','muted'),
                ('Red-Blue','RdBu'),
                ('Set1','Set1'),
                ('Set2','Set2'),
                ('Set3','Set3'),
                ('husl','husl'),
                ('spring', 'spring'),
                ('summer', 'summer'),
                ('ocean', 'ocean'),
            ],
            half_spine=True,
            save=False,
        )

def make_density_plot(X, Y, df, force_dtype={}, **params):
    pass

def make_box_plot_seaborn(Xs, Y, df, force_dtype={}, **params):
    plt.figure(figsize=(params['Figsize_x'], params['Figsize_y']))
    if params['color_palette'] == '':
        with sn.color_palette():
            if isinstance(Xs, str):
                ax = sn.boxplot(x=Xs, y = Y, data=df)
            else:
                ax = sn.boxplot(x=Xs[1], y = Y, data=df,hue=Xs[0])
    else:
        key = Xs if isinstance(Xs, str) else Xs[0]
        with sn.color_palette(params['color_palette'], df[key].nunique()):
            if isinstance(Xs, str):
                ax = sn.boxplot(x=Xs, y = Y, data=df)
            else:
                ax = sn.boxplot(x=Xs[1], y = Y, data=df,hue=Xs[0])
    ax.set_title(params['Title'])
    if 'half_spine' in params:
        ax.spines["top"].set_visible(not params['half_spine'])  
        ax.spines["right"].set_visible(not params['half_spine'])
    ax.set_xlabel(params['xlabel'])
    ax.set_ylabel(params['ylabel'])
    fig = ax.get_figure()
    plt.show(ax)
    if params['save']:
        fig.savefig('saved_boxplot_plot.png')

def make_interactive_boxplot(Xs, Y, df, force_dtype={}):
    def plot(**params):
        make_box_plot_seaborn(Xs, Y, df, force_dtype, **params)
    if isinstance(Xs, str):
        widgets.interact(
            plot,
            Title="",
            xlabel=Xs,
            ylabel=Y,
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
            color_palette=[
                ('default',''),
                ('muted','muted'),
                ('Red-Blue','RdBu'),
                ('Set1','Set1'),
                ('Set2','Set2'),
                ('Set3','Set3'),
                ('husl','husl'),
                ('spring', 'spring'),
                ('summer', 'summer'),
                ('ocean', 'ocean'),
            ],
            half_spine=True,
            save=False,
        )
    elif len(Xs) == 2:
        widgets.interact(
            plot,
            Title="",
            xlabel=Xs[1],
            ylabel=Y,
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
            color_palette=[
                ('default',''),
                ('muted','muted'),
                ('Red-Blue','RdBu'),
                ('Set1','Set1'),
                ('Set2','Set2'),
                ('Set3','Set3'),
                ('husl','husl'),
                ('spring', 'spring'),
                ('summer', 'summer'),
                ('ocean', 'ocean'),
            ],
            half_spine=True,
            save=False,
        )
    else:
        raise NotImplementedError()

def make_violin_plot_seaborn(Xs, Y, df, force_dtype={}, **params):
    plt.figure(figsize=(params['Figsize_x'], params['Figsize_y']))
    if params['color_palette'] == '':
        with sn.color_palette():
            if isinstance(Xs, str):
                ax = sn.violinplot(x=Xs, y = Y, data=df)
            else:
                ax = sn.violinplot(x=Xs[1], y = Y, data=df,hue=Xs[0])
    else:
        key = Xs if isinstance(Xs, str) else Xs[0]
        with sn.color_palette(params['color_palette'], df[key].nunique()):
            if isinstance(Xs, str):
                ax = sn.violinplot(x=Xs, y = Y, data=df)
            else:
                ax = sn.violinplot(x=Xs[1], y = Y, data=df,hue=Xs[0])
    ax.set_title(params['Title'])
    if 'half_spine' in params:
        ax.spines["top"].set_visible(not params['half_spine'])  
        ax.spines["right"].set_visible(not params['half_spine'])
    ax.set_xlabel(params['xlabel'])
    ax.set_ylabel(params['ylabel'])
    fig = ax.get_figure()
    plt.show(ax)
    if params['save']:
        fig.savefig('saved_violin_plot.png')
        
        
def make_interactive_violin(Xs, Y, df, force_dtype={}):
    def plot(**params):
        make_violin_plot_seaborn(Xs, Y, df, force_dtype, **params)
    if isinstance(Xs, str):
        widgets.interact(
            plot,
            Title="",
            xlabel=Xs,
            ylabel=Y,
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
            color_palette=[
                ('default',''),
                ('muted','muted'),
                ('Red-Blue','RdBu'),
                ('Set1','Set1'),
                ('Set2','Set2'),
                ('Set3','Set3'),
                ('husl','husl'),
                ('spring', 'spring'),
                ('summer', 'summer'),
                ('ocean', 'ocean'),
            ],
            half_spine=True,
            save=False,
        )
    elif len(Xs) == 2:
        widgets.interact(
            plot,
            Title="",
            xlabel=Xs[1],
            ylabel=Y,
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
            color_palette=[
                ('default',''),
                ('muted','muted'),
                ('Red-Blue','RdBu'),
                ('Set1','Set1'),
                ('Set2','Set2'),
                ('Set3','Set3'),
                ('husl','husl'),
                ('spring', 'spring'),
                ('summer', 'summer'),
                ('ocean', 'ocean'),
            ],
            half_spine=True,
            save=False,
        )