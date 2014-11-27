__author__ = 'Horea Christian'
from os import path, makedirs
from shutil import move
from datetime import date, datetime
import csv

def mk_newfilter(filtername, field_names, filterdir, globaldata):
    lefilter = globaldata+filterdir+filtername+'.csv'
    jzt=datetime.now()
    time = str(date.today())+str(jzt.hour)+str(jzt.minute)+str(jzt.second)
    if path.isdir(globaldata+filterdir):
        pass
    else: makedirs(globaldata+filterdir)
    if path.isfile(lefilter):
        if path.isdir(globaldata+filterdir+'.backup'):
            pass
        else: makedirs(globaldata+filterdir+'.backup')
        move(lefilter, globaldata+filterdir+'.backup/'+time+filtername+'.csv')
        print('moved '+lefilter+' pre-existing filter to backup location')
    else: pass
    filterfile = open(lefilter, 'w')
    filterwriter = csv.writer(filterfile, delimiter=',')
    #print prim_data
    filterwriter.writerow(list(field_names)+['field names'])
    filterwriter.writerow(list([0]*(len(field_names)))+['metadata'])
    filterwriter.writerow(list([0]*(len(field_names)))+['identificator'])
    filterwriter.writerow(list([0]*(len(field_names)))+['reverse scoring'])
    filterwriter.writerow(list([0]*(len(field_names)))+['gender'])
    filterwriter.writerow(list([0]*(len(field_names)))+['age'])
    filterwriter.writerow(list([0]*(len(field_names)))+['sexuality'])
    filterwriter.writerow(list([0]*(len(field_names)))+['soi-r'])
    filterwriter.writerow(list([0]*(len(field_names)))+['soi-r behaviour facet'])
    filterwriter.writerow(list([0]*(len(field_names)))+['soi-r attitude facet'])
    filterwriter.writerow(list([0]*(len(field_names)))+['soi-r desire facet'])
    filterwriter.writerow(list([0]*(len(field_names)))+['ras'])
    filterwriter.writerow(list([0]*(len(field_names)))+['tipi'])
    filterwriter.writerow(list([0]*(len(field_names)))+['tipi extraversion'])
    filterwriter.writerow(list([0]*(len(field_names)))+['tipi agreeableness'])
    filterwriter.writerow(list([0]*(len(field_names)))+['tipi conscientiousness'])
    filterwriter.writerow(list([0]*(len(field_names)))+['tipi emotional stability'])
    filterwriter.writerow(list([0]*(len(field_names)))+['tipi openness to experiences'])
    filterfile.close()
