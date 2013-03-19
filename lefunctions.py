__author__ = 'Horea Christian'
import numpy as np

def means_from_id(lelist):
    lelist = lelist[lelist[:,0].argsort()] #sort by file name
    uniques = list(set(lelist[:,0])) # get unique names
    b = np.empty((len(uniques), len(lelist[0])), dtype = 'S12')   # create destination array for means
    for i,s in enumerate(uniques):
        m = lelist[:,0] == s
        b[i] = [s] + [lelist[m,j].astype(float).mean() for j in [1,2]] + [int(lelist[m,3].astype(float).mean())]
    return b