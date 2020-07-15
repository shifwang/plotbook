import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.offline as pyo
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
