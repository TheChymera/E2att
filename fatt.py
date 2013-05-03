#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
from os import listdir, path
from lefunctions import open_csv
from scipy.stats import ttest_ind, pearsonr
import pandas as pd
import numpy as np

globalpath = '~/Data/shared/2att/' #root of results
bh_results = 'bh/' # behavioural test results
cq_results = 'cq/' # questionnaire results

globalpath = path.expanduser(globalpath)
bhpath = globalpath + bh_results
cqpath = globalpath + cq_results

files = [lefile for lefile in listdir(bhpath) if lefile.endswith('.csv')]
ids = [t.split('_',2)[0]+'_'+t.split('_',2)[1] for t in files]
ids = np.unique(ids)
conts = pd.DataFrame([])

for i in ids:
	print i
	cont = open_csv(bhpath+i+'_p')
	cont = pd.DataFrame(cont[1:], columns=cont[0])
	cont['score'] = cont['score'].astype(np.float64)
	cont['RT'] = cont['RT'].astype(np.float64)
	cont['session'] = cont['session'].astype(np.float64)
	#cont.index = cont['picture']
	#cont = cont.pivot(index='session', columns='picture', values='score')
	#cont = pd.DataFrame({'count':cont.groupby('picture').size()}).reset_index()
	#lala = lambda x: (x - x.mean()) / x.std()
	#cont = cont.groupby(['picture'], as_index=True).mean()
	cont = cont.set_index('picture', 'session').sort()
	meas_id = [1,2,3] * int(len(cont.index) / 3)
	cont['measurement']=''
	cont = cont.reset_index().set_index(['measurement', meas_id])
	lemeans = pd.DataFrame([])
	lemeans['picture'] = ''
	for n in set(cont.set_index('session').index):
		print cont[(cont['session'] == n)]['picture']
		print cont[(cont['picture'] == cont[(cont['session'] == n)]['picture'])]
		cont.ix[(cont['session'] == n), 'score'] = cont[(cont['session'] == n)]['score']/cont[(cont['picture'] == cont[(cont['session'] == n)]['picture'])].mean()
		#print cont[(cont['session'] == n)]
		#means = pd.DataFrame([])
		#means['picture'] = n
		#print means
		#cont[cont['picture'] == n] = (cont[cont['picture'] == n] - cont[cont['picture'] == n].mean()) / cont[cont['picture'] == n].std()
	print cont
