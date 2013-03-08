#!/usr/bin/env python
__author__ = 'Horea Christian' #if you contribute add your name to the end of this list

from list_op import lefilter, reverse_score, calc_score
import numpy as np
from import_export import export_data

leresults=[]

reverse_score()
for i in ['identificator', 'gender', 'age', 'sexuality']:
    values = lefilter(i)
    leresults=leresults+[[i] + values.tolist()]
for i in ['soi-r', 'soi-r behaviour facet', 
          'soi-r attitude facet', 'soi-r desire facet', 'ras', 
          'tipi extraversion', 'tipi agreeableness', 'tipi conscientiousness', 
          'tipi emotional stability', 'tipi openness to experiences']:
    values = calc_score(i)
    leresults = leresults+[[i] + values.tolist()]
leresults = np.array(leresults)
export_data(leresults) 