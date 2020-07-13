import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt

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

def make_beeswamp_plot(X, Y, df, force_dtype={}, **params):
    ax = sn.swarmplot(x=X, y = Y, data=df)
    fig = ax.get_figure()
    plt.show(ax)

def make_density_plot(X, Y, df, force_dtype={}, **params):
    pass

def make_box_plot_seaborn(X, Y, df, force_dtype={}, **params):
    ax = sn.boxplot(df[X], df[Y])
    fig = ax.get_figure()
    plt.show(fig)

def make_violin_plot_seaborn(X, Y, df, force_dtype={}, **params):
    ax = sn.violinplot(df[X], df[Y])
    fig = ax.get_figure()
    plt.show(fig)