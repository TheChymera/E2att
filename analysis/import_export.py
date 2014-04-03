__author__ = 'Horea Christian' #if you contribute add your name to the end of this list
from os import path
import csv
import numpy as np
from filter_gen import mk_newfilter

#input files
newfilter='' # empty unless you want to create a new filter file, specify relative to globaldata + filterdir
filename = 'cmp22_02_2013' # survey results from said date
filtername = 'default' #filter file
globaldata = '~/Data/shared/2att/cq/' #global data folder
localdata = 'localdata/' #local data folder
filterdir= 'filters/' #location of filter files
outputname = 'res_'+filename

globaldata = path.expanduser(globaldata)
if path.isfile(localdata+filename):
    outputpath = localdata + outputname + '.csv'
    datapath = localdata + filename + '.csv'
    filterpath = localdata + filterdir + filtername + '.csv'
else: 
    outputpath = globaldata + outputname + '.csv'
    datapath = globaldata+filename + '.csv'
    filterpath = globaldata+filterdir+filtername + '.csv'

def get_data():
    datafile = open(datapath, 'r')
    readdata = csv.reader(datafile, delimiter =',')
    prim_data = []
    for row in readdata:
        prim_data.append(row)
    datafile.close()
    field_names = np.array(prim_data[0][:])
    prim_data = np.array(prim_data[1:])
    
    #write a filter
    if not path.isfile(filterpath):
        mk_newfilter(filtername, field_names, filterdir, globaldata)
    elif newfilter == '':
        pass
    else:
        mk_newfilter(newfilter, field_names, filterdir, globaldata)
    
    filterfile = open(filterpath, 'r')
    readfilter = csv.reader(filterfile, delimiter =',')
    filters = []
    for row in readfilter:
        filters.append(row)
    filterfile.close()
    filters = np.array(filters)
    
    return prim_data, filters, field_names

def export_data(leresults):
    outputfile = open(outputpath,'w')
    outputwriter = csv.writer(outputfile, delimiter=',')
#    outputwriter.writerow(['identificator', 'gender', 'age', 'sexuality', 'soi-r', 'ras', 
#                           'tipi', 'extraversion', 'agreeableness', 'conscientiousness', 
#                           'emotional stability', 'openness to experiences'])
    for i in leresults:
        outputwriter.writerow(i)
    outputfile.close()