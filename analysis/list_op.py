__author__ = 'Horea Christian' #if you contribute add your name to the end of this list
import numpy as np
from import_export import get_data
soir_max = 9 #maximum numerical score in SOI-R items
ras_max = 5 #maximum numerical score in RAS items
tipi_max = 7 #maximum numerical score in TIPI items
divide = np.array([['ras', 7],['tipi', 2]]) #what scores need to be divided by what numbers


def lefilter(keep=None):
    data, filters, _ = get_data()
    mask = filters[:,-1] == keep
    lefilter = filters[mask][:,:-1]
    value = data[:,lefilter.astype(np.bool)[0]]
    if keep != 'gender':
        value = value.astype(np.integer)
    return value

def reverse_score():
    data, filters, _ = get_data()
    data_nn = data[0:,:]
    lefilter = filters[filters[:,-1] == 'reverse scoring'][0]
    soirfilter = filters[filters[:,-1] == 'soi-r'][0]
    rasfilter = filters[filters[:,-1] == 'ras'][0]
    tipifilter = filters[filters[:,-1] == 'tipi'][0]
#    mask = lefilter != '0'
#    newfilter = filters[:,mask]
#    newdata = data[:,mask[:-1]].astype(np.integer)
    for ixr,row in enumerate(data_nn):
        for ixe, el in enumerate(row):
            if lefilter[ixe] == '1':
                if soirfilter[ixe] == '1':
                    data_nn[ixr,ixe] = soir_max + 1 - el.astype(np.integer)
                elif rasfilter[ixe] == '1':
                    data_nn[ixr,ixe] = ras_max + 1 - el.astype(np.integer)
                elif tipifilter[ixe] == '1':
                    data_nn[ixr,ixe] = tipi_max + 1 - el.astype(np.integer)
    return data_nn

def calc_score(param=None):
    data, filters, _ = get_data()
    mask = filters[:,-1] == param
    lefilter = filters[mask][:,:-1]
    values = data[:,lefilter.astype(np.bool)[0]].astype(np.integer)
    value = np.sum(values, axis=1)
    if param.startswith('tipi'):
        value = value / divide[divide[:,0] == 'tipi',:][:,-1].astype(np.integer)
    elif param.startswith('ras'):
        value = value / divide[divide[:,0] == 'ras',:][:,-1].astype(np.integer)
    return value