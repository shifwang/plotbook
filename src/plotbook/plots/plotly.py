import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.offline as pyo
# Set notebook mode to work in offline
pyo.init_notebook_mode()

def make_sunburst_plot(X, Y, df, force_dtype={}):
    '''make sunburst plot'''
    output = df.apply(lambda row: (row[X], row[Y]), axis=1)
    values, counts = np.unique(output, return_counts=True)
    x = pd.Series([value[0] for value in values])
    y = pd.Series([value[1] for value in values])

    out = pd.DataFrame({'X':x, 'Y':y, 'counts':counts})
    fig = px.sunburst(
        out,
        path=['X', 'Y'],
        values='counts',
    )
    fig.show()
