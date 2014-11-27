#!/usr/bin/env python
__author__ = 'Horea Christian' #if you contribute add your name to the end of this list

from list_op import lefilter, reverse_score, calc_score
from import_export import export_data

leresults=[]

reverse_score()
for i in ['identificator', 'gender', 'age', 'sexuality']:
    values = lefilter(i)
    leresults=leresults+[[i] + values.tolist()]

#FIX GLITCH - the output of lefilter() contains single element lists, we make them normal elements here
for ixr, row in enumerate(leresults):
    for ixe, el in enumerate(row):
        if len(el)==1:
            leresults[ixr][ixe] = el[0]
#END FIX GLITCH

for i in ['soi-r', 'soi-r behaviour facet', 
          'soi-r attitude facet', 'soi-r desire facet', 'ras', 
          'tipi extraversion', 'tipi agreeableness', 'tipi conscientiousness', 
          'tipi emotional stability', 'tipi openness to experiences']:
    values = calc_score(i)
    leresults = leresults+[[i] + values.tolist()]
export_data(leresults) 