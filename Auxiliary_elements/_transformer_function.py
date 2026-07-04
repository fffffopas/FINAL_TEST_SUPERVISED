import pandas as pd
import numpy as np

def to_num_nbin(X):
    pd.set_option('future.no_silent_downcasting', True)
    X = X.replace(r"No.*", 0, regex=True)
    X = X.replace("Yes", 1).astype(int)
    return X

def to_delete(X):
    return X.drop(["customerID"], axis=1)