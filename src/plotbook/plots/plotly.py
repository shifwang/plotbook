import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.offline as pyo
import ipywidgets as widgets
# Set notebook mode to work in offline
pyo.init_notebook_mode()

def make_sunburst_plot(Xs, Y, df, force_dtype={}):
    '''make sunburst plot'''
    if isinstance(Xs, str):
        Xs = [Xs]
    if len(Xs) == 1:
        X = Xs[0]
        output = df.apply(lambda row: (row[X], row[Y]), axis=1)
        values, counts = np.unique(output, return_counts=True)
        x = pd.Series([value[0] for value in values])
        y = pd.Series([value[1] for value in values])

        out = pd.DataFrame({X:x, Y:y, 'counts':counts})
        fig = px.sunburst(
            out,
            path=[X, Y],
            values='counts',
        )
    elif len(Xs) == 2:
        X1 = Xs[0]
        X2 = Xs[1]
        output = df.apply(lambda row: (row[X1], row[X2], row[Y]), axis=1)
        values, counts = np.unique(output, return_counts=True)
        x1 = pd.Series([value[0] for value in values])
        x2 = pd.Series([value[1] for value in values])
        y = pd.Series([value[2] for value in values])

        out = pd.DataFrame({X1:x1, X2:x2, Y:y, 'counts':counts})
        fig = px.sunburst(
            out,
            path=[X1, X2, Y],
            values='counts',
        )
            
    fig.show()

def make_interactive_heatmap(Xs, Y, df, force_dtype={}):
    if isinstance(Xs, str):
        Xs = [Xs]
    def make_heatmap(**params):
        if params['hist_x']:
            params['hist_x'] = "histogram"
        else:
            params['hist_x'] = None
        if params['hist_y']:
            params['hist_y'] = "histogram"
        else:
            params['hist_y'] = None
        fig = px.density_heatmap(
            df,
            x=Xs[-1],
            y=Y,
            marginal_x=params['hist_x'],
            marginal_y=params['hist_y'],
            title=params['Title'],
            width=params['Figsize_x'] * 100,
            height=params['Figsize_y'] * 100,
        )
        fig.update_layout(
            xaxis_title=params['xlabel'],
            yaxis_title=params['ylabel'],
        )
        fig.show()
        if params['save']:
            fig.write_image("saved_plotly_heatmap.png")
    if len(Xs) == 1:
        widgets.interact(
            make_heatmap,
            Title="",
            xlabel=Xs[-1],
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
            hist_x=True,
            hist_y=True,
            save=False,
        )