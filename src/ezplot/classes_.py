import pandas as pd
import visions as v
from .plots import (
    make_occur_map,
    make_occur_map_2
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

def auto_plot_single(X, Y, df, force_dtype={}, infer_dtype=False):
    ''' Plot X vs Y with knowledge that X and Y are single dimension.
    '''
    if infer_dtype:
        types_dict = v.infer_frame_type(df, typeset=v.typesets.CompleteSet())
        for colname, dtype in types_dict.items():
            if colname not in force_dtype:
                force_dtype[colname] = dtype
    
    set1 = {'String', 'Categorical', 'Integer'}

    if (
        (str(force_dtype[X]) in set1),
        (str(force_dtype[Y]) in set1)
    ):
        if df[X].nunique() > len(X) // 2:
            UserWarning("column {X} has too many unique values.")
        if df[Y].nunique() > len(Y) // 2:
            UserWarning("column {Y} has too many unique values.")
        make_occur_map(X, Y, df, force_dtype=force_dtype)
        make_occur_map_2(X, Y, df, force_dtype=force_dtype)
        
    pass
