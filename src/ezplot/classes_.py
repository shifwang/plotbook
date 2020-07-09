import pandas as pd
import visions as v
import ipywidgets as widgets
import numpy as np
from .plots import (
    make_occur_plot,
    make_occur_plot_2,
    make_sunburst_plot,
    make_line_plot,
    make_scatter_plot,
)


def auto_plot(X : list, Y : list, df, infer_dtype=True, force_dtype={}):
    ''' automatically plot the relationship between X and Y
    Parameters
    ----------

    X : list of strs, the columns in df that correspond to covariates

    Y : list of strs, the columns in df that correspond to targets
    
    df : pands dataframe, the data
    
    infer_type : boolean, whether to infer dtypes from df
    
    force_dtype : dict, keys are colnames and values are the one of the
        following:
        {Boolean, Categorical, Complex, Count, Date, DateTime, File,
        Float, Generic, Geometry, IPAddress, Image, Integer, Object,
        Ordinal, Path, String, Time, TimeDelta, URL, UUID}
    '''
    if infer_dtype:
        types_dict = v.infer_frame_type(df, typeset=v.typesets.CompleteSet())
        for colname, dtype in types_dict.items():
            if colname not in force_dtype:
                force_dtype[colname] = dtype
        
    if len(X) == 1 and len(Y) == 1:
        auto_plot_single(
            X[0],
            Y[0],
            df,
            force_dtype=force_dtype,
            infer_dtype=False,
        )
    else:
        raise NotImplementedError()

def tab_show(X, Y, df,
             force_dtype={},
             plot_names=[],
             plot_functions=[],
             scores=[]):
    ''' Show figures in a tab widget
    '''
    tabs = []
    orders = len(scores) - 1 - np.argsort(scores)
    for i in orders:
        tabs.append(widgets.Output())
    tab = widgets.Tab(children = tabs)
    for rank, i in enumerate(orders):
        tab.set_title(i, plot_names[rank])
    display(tab)
    for rank, i in enumerate(orders):
        with tabs[i]:
            plot_func = plot_functions[rank]
            plot_func(X, Y, df, force_dtype=force_dtype)

def auto_plot_single(X, Y, df, force_dtype={}, infer_dtype=False):
    ''' Plot X vs Y with knowledge that X and Y are single dimension.
    '''
    if infer_dtype:
        types_dict = v.infer_frame_type(df, typeset=v.typesets.CompleteSet())
        for colname, dtype in types_dict.items():
            if colname not in force_dtype:
                force_dtype[colname] = dtype
    
    plot_names = []
    plot_functions = []
    scores = []
    set1 = {'String', 'Categorical', 'Integer'}

    if (
        (str(force_dtype[X]) in set1) and
        (str(force_dtype[Y]) in set1)
    ):
        n_warning = 0
        if df[X].nunique() > len(X) // 2:
            n_warning += 1
            UserWarning("column {X} has too many unique values.")
        if df[Y].nunique() > len(Y) // 2:
            n_warning += 1
            UserWarning("column {Y} has too many unique values.")
        
        plot_names += ['Sunburst', 'Occurence Plot', 'Heatmap']
        plot_functions +=[
            make_sunburst_plot,                  
            make_occur_plot,
            make_occur_plot_2,
        ]
        scores += [
            1 - n_warning * 0.1,
            0.9 - n_warning * 0.1,
            0.8 - n_warning * 0.1,
        ]
    set2 = {'Integer', 'Float'}
    
    if (
        (str(force_dtype[X]) in set2) and
        (str(force_dtype[X]) in set2)
    ):
        X_overlap = df.groupby(X)[Y].count().max()
        if X_overlap > 1:
            score_line_plot = 0
        else:
            score_line_plot = 1
        if X_overlap > len(df[X]) // 20:
            score_scatter_plot = 0.8
        else:
            score_scatter_plot = 0.9
        plot_names += ['Scatter Chart', 'Line Chart']
        plot_functions +=[
            make_scatter_plot,
            make_line_plot,
        ]
        scores += [
            score_scatter_plot,
            score_line_plot,
        ]
        pass
    tab_show(X, Y, df, force_dtype, plot_names, plot_functions, scores)
    pass
