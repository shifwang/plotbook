import pandas as pd

def auto_plot(self, X -> list, Y -> list, df):
    ''' automatically plot the relationship between X and Y
    Parameters
    ----------

    X : list of strs, the columns in df that correspond to covariates

    Y : list of strs, the columns in df that correspond to targets
    
    df : pands dataframe, the data
    '''
    if len(X) == 1 and len(Y) == 1:
        return auto_plot_single(X, Y, df)
    else:
        raise NotImplementedError()

def auto_plot_single(X, Y, df):
    ''' Plot X vs Y with knowledge that X and Y are single dimension.
    '''
    pass
