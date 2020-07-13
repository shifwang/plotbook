import pandas as pd
import visions as v
import ipywidgets as widgets
import numpy as np
from .plots import (
    make_occur_plot,
    make_occur_plot_2,
    make_sunburst_plot,
    make_interactive_scatter_plot,
    make_interactive_line_plot,
    make_pie_chart,
    make_beeswamp_plot,
    make_box_plot,
    make_density_plot,
    make_violin_plot_seaborn,
    make_box_plot_seaborn,
)


def auto_plot(
    X : str,
    Y : str,
    df : pd.DataFrame,
    legend=None,
    facet=None,
    infer_dtype=True,
    force_dtype={},
):
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
    elif len(X) == 2 and len(Y) == 1:
        auto_plot_
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
            make_interactive_scatter_plot,
            make_interactive_line_plot,
        ]
        scores += [
            score_scatter_plot,
            score_line_plot,
        ]
        pass
    set3 = {'String', 'Categorical'}
    if (
        (str(force_dtype[X]) in set2) and
        (str(force_dtype[Y]) in set3)
    ):
        X, Y = Y, X # swap X, Y when Y is categorical and X is numeric

    if (
        (str(force_dtype[X]) in set1) and 
        (str(force_dtype[Y]) in set2)
    ):
        # X is categorical and Y is numeric
        n_class = df[X].nunique()
        if df[Y].min() > 0 and n_class == len(df[X]):
            plot_names += ['Pie Chart']
            plot_functions += [make_pie_chart]
        
            scores += [
                0 if n_class == 1 else 1/(n_class - 1)
            ]
        min_obs = df[[X, Y]].groupby(X)[Y].count().min()
        if min_obs > 1:
            plot_names += ['Box Plot', 'Beeswamp Chart', 'Violin Chart']
            plot_functions += [
                make_box_plot_seaborn,
                make_beeswamp_plot,
                make_violin_plot_seaborn,
            ]
            scores += [
                1,
                1/max(min_obs/20, 1),
                1 - min_obs ** -1 + 0.01,
            ]
            if n_class <= 3 and min_obs > 20:
                plot_names += ['Density Plot']
                plot_functions += [make_density_plot]
                scores += [1]

    tab_show(X, Y, df, force_dtype, plot_names, plot_functions, scores)
    pass
