#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
from os import listdir, path
from lefunctions import open_csv
from scipy.stats import ttest_ind, sem
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from pylab import figure, show, errorbar, setp, legend
from matplotlib import axis

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
spec = ['6245247_f']
h_dist = ['1236345_f','6779353_f','7310001_f','7714775_m','7816097_m','7865828_m','7922847_m']
l_dist = ['1975801_m','4724273_f','6268973_m','8963557_f','8286497_m','8963557_m','9651558_m','8240877_m','6887665_m','5559429_f','8582941_f','8582941_m','9302438_f','4276763_f','3878418_m','3537898_f','1247497_f','8717741_m','4744495_f','7117377_m']
test = ['chr1_f','chr2_f']
id_list = l_dist

for i in id_list:
	print i
	ratings = open_csv(bhpath+i+'_p')
	ratings = pd.DataFrame(ratings[1:], columns=ratings[0], dtype=float)
	ratings = ratings.groupby('picture').mean()    
	sorted_scores = sorted(ratings['score'])
	score_top, score_bottom = sorted_scores[-20], sorted_scores	[19]

	cont = open_csv(bhpath+i+'_wm')
	cont = pd.DataFrame(cont[1:], columns=cont[0])
	cont['rateL'] = cont['rateL'].astype(np.float64)
	cont['RTL'] = cont['RTL'].astype(np.float64)
	cont['orderL'] = cont['orderL'].astype(np.float64)
	cont['rateR'] = cont['rateR'].astype(np.float64)
	cont['RTR'] = cont['RTR'].astype(np.float64)
	cont['orderR'] = cont['orderR'].astype(np.float64)
	cont['RT'] = cont['RT'].astype(np.float64)
	cont['session'] = cont['session'].astype(np.float64)
	cont = cont[cont['RT'] >=0]
	cont.ix[cont['isstimleft'] == 'False', 'isstimleft'] = False
	cont.ix[cont['isstimleft'] == 'True', 'isstimleft'] = True
	cont['ID'] = i	
	cont1 = cont[(cont['isstimleft'] == False) & (cont['keypress'] == 'right')]
	cont2 = cont[(cont['isstimleft'] == True) & (cont['keypress'] == 'left')]
	cont = pd.concat([cont1,cont2])
	cont['block'] = ''
	cont.ix[(cont['rateL'] >= score_top) & (cont['rateR'] >= score_top), 'block'] = 'aa'
	cont.ix[(cont['rateL'] >= score_top) & (cont['rateR'] <= score_bottom), 'block'] = 'au'
	cont.ix[(cont['rateL'] <= score_bottom) & (cont['rateR'] >= score_top), 'block'] = 'ua'
	cont.ix[(cont['rateL'] <= score_bottom) & (cont['rateR'] <= score_bottom), 'block'] = 'uu'
	conts = pd.concat([conts, cont], ignore_index=True)
	#cat1 = cont[cont['block']=='aa']
	#cat2 = cont[cont['block']=='uu']
	#print ttest_ind(cat1['RT'], cat2['RT'])

ids = sorted(list(set(conts.set_index('ID').index)))
pos_ids = np.arange(len(ids))

aa_means = conts[(conts['block'] == 'aa')].groupby('ID')['RT'].mean()
aa_std = conts[(conts['block'] == 'aa')].groupby('ID')['RT'].aggregate(sem)
aa_t_means = conts[(conts['block'] == 'aa')]['RT'].mean()
aa_t_std = sem(conts[(conts['block'] == 'aa')]['RT'])

#cat1 = conts[conts['block']=='aa']
#cat2 = conts[conts['block']=='uu']
#print ttest_ind(cat1['RT'], cat2['RT'])

uu_means = conts[(conts['block'] == 'uu')].groupby('ID')['RT'].mean()
uu_std = conts[(conts['block'] == 'uu')].groupby('ID')['RT'].aggregate(sem)
uu_t_means = conts[(conts['block'] == 'uu')]['RT'].mean()
uu_t_std = sem(conts[(conts['block'] == 'uu')]['RT'])

fig = figure(figsize=(pos_ids.max(), 5), dpi=80,facecolor='#eeeeee',tight_layout=True)
ax=fig.add_subplot(1,1,1)
width = 0.3
ax.yaxis.grid(True, linestyle='-', which='major', color='#dddddd',alpha=0.5, zorder = 1)

aa_bar = plt.bar(pos_ids, aa_means, width ,color='g', alpha=0.4, zorder = 1)
aa_err = errorbar(pos_ids+(width/2), aa_means, yerr=aa_std, ecolor='0.5', elinewidth='3', capsize=0, linestyle='None', zorder = 2)
aa_t_bar = plt.bar(pos_ids[-1]+1, aa_t_means, width ,color='g', alpha=0.8, zorder = 1)
aa_err = errorbar(pos_ids[-1]+1+(width/2), aa_t_means, yerr=aa_t_std, ecolor='0.1', elinewidth='3', capsize=0, linestyle='None', zorder = 2)

uu_bar = plt.bar(pos_ids+width, uu_means, width ,color='m', alpha=0.4, zorder = 1)
uu_err = errorbar(pos_ids+(width*3/2), uu_means, yerr=uu_std, ecolor='0.5', elinewidth='3', capsize=0, linestyle='None', zorder = 2)
uu_t_bar = plt.bar(pos_ids[-1]+1+width, uu_t_means, width ,color='m', alpha=0.8, zorder = 1)
uu_err = errorbar(pos_ids[-1]+1+(width*3/2), uu_t_means, yerr=uu_t_std, ecolor='0.1', elinewidth='3', capsize=0, linestyle='None', zorder = 2)

ids=ids+['total']
pos_ids = np.arange(len(ids))
ax.set_xlim(0, pos_ids.max())
ax.set_ylim(0, 1.1)
ax.set_ylabel(r'$\mathsf{\overline{RT}}$ [s]', fontsize=13)
ax.set_xlabel('Participant ID')
ax.set_xticks(pos_ids + width)
ax.set_xticklabels(ids,fontsize=9,rotation=30)
for tick in ax.axes.get_xticklines():
	tick.set_visible(False)
axis.Axis.zoom(ax.xaxis, -0.5)
legend((aa_t_bar,uu_t_bar),('Only attractive faces','Only unattractive faces'), 'upper right', shadow=False, frameon=False, prop= FontProperties(size='11'))
show()
