__author__ = 'Horea Christian'
import numpy as np

def means_from_id(lelist):
    lelist = lelist[lelist[:,0].argsort()] #sort by file name
    uniques = list(set(lelist[:,0])) # get unique names
    b = np.empty((len(uniques), len(lelist[0])), dtype = 'S24')   # create destination array for means
    for i,s in enumerate(uniques):
        m = lelist[:,0] == s
        b[i] = [s] + [lelist[m,j].astype(float).mean() for j in [1,2]] + [int(lelist[m,3].astype(float).mean())]
    return b

def save_csv(filename, firstline=[]):
    from os import path, makedirs
    from shutil import move
    from datetime import date, datetime
    import csv
    filename
    jzt=datetime.now()
    time = str(date.today())+'_'+str(jzt.hour)+str(jzt.minute)+str(jzt.second)
    if path.isfile(filename):
        if path.isdir(path.dirname(filename)+'/.backup'):
            pass
        else: makedirs(path.dirname(filename)+'/.backup')        
        newname = path.dirname(filename)+'/.backup/'+path.splitext(path.basename(filename))[0]+'_'+time+path.splitext(path.basename(filename))[1]
        move(filename, newname)
        print 'moved pre-existing data file '+ filename +' to backup location ('+newname+')'
    else: pass
    datafile = open(filename, 'a')
    datawriter = csv.writer(datafile, delimiter=',')
    #print first line
    datawriter.writerow(firstline)
    return datawriter, datafile