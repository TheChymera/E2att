#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
from os import listdir, path
from lefunctions import get_dataframes
from scipy.stats import ttest_ind, sem
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from pylab import figure, show, errorbar, setp, legend
from matplotlib import axis
from collections import defaultdict

globalpath = '~/Data/shared/2att/' #root of results
bh_results = 'bh/' # behavioural test results
cq_results = 'cq/' # questionnaire results

globalpath = path.expanduser(globalpath)
bhpath = globalpath + bh_results
cqpath = globalpath + cq_results

files = [lefile for lefile in listdir(bhpath) if lefile.endswith('.csv')]
ids = [t.split('_',2)[0]+'_'+t.split('_',2)[1] for t in files]
ids = np.unique(ids)
spec = ['6245247_f']
h_dist = ['1236345_f','6779353_f','7310001_f','7714775_m','7816097_m','7865828_m','7922847_m']
l_dist = ['1975801_m','4724273_f','6268973_m','8963557_f','8286497_m','8963557_m','9651558_m','8240877_m','6887665_m','5559429_f','8582941_f','8582941_m','9302438_f','4276763_f','3878418_m','3537898_f','1247497_f','8717741_m','4744495_f','7117377_m']
test = ['chr1_f','chr2_f']
id_list = l_dist
isspec = True

conts = get_dataframes(id_list, bhpath)
if isspec:
	spec_conts = get_dataframes(spec, bhpath)
	meanscont = spec_conts.groupby('subblock').mean()
	print(meanscont)
	cat1 = spec_conts[spec_conts['subblock']=='aus+sua']
	cat2 = spec_conts[spec_conts['subblock']=='uas+sau']
	print(ttest_ind(cat1['RTdiff'], cat2['RTdiff']))

meanscont = conts.groupby('subblock').mean()
print(meanscont)
cat1 = conts[conts['subblock']=='aus+sua']
cat2 = conts[conts['subblock']=='uas+sau']
print(ttest_ind(cat1['RTdiff'], cat2['RTdiff']))

ids = sorted(list(set(conts.set_index('ID').index)))
pos_ids = np.arange(len(ids))

#sa_df = conts[(conts['subblock'] == 'uas+sau')]
#sa_di = defaultdict(list)
#for x, y in zip(sa_df['RTdiff'], sa_df['ID']): sa_di[y].append(x)
#sa_li = [i for k, i in sa_di.iteritems()]

#su_df = conts[(conts['subblock'] == 'aus+sua')]
#su_di = defaultdict(list)
#for x, y in zip(su_df['RTdiff'], su_df['ID']): su_di[y].append(x)
#su_li = [i for k, i in su_di.iteritems()]

sa_means = conts[(conts['subblock'] == 'uas+sau')].groupby('ID')['RTdiff'].mean()
sa_std = conts[(conts['subblock'] == 'uas+sau')].groupby('ID')['RTdiff'].aggregate(sem)

su_means = conts[(conts['subblock'] == 'aus+sua')].groupby('ID')['RTdiff'].mean()
su_std = conts[(conts['subblock'] == 'aus+sua')].groupby('ID')['RTdiff'].aggregate(sem)

sa_means = conts[(conts['subblock'] == 'uas+sau')].groupby('ID')['RTdiff'].mean()
sa_std = conts[(conts['subblock'] == 'uas+sau')].groupby('ID')['RTdiff'].aggregate(sem)
sa_t_means = conts[(conts['subblock'] == 'uas+sau')]['RTdiff'].mean()
sa_t_std = sem(conts[(conts['subblock'] == 'uas+sau')]['RTdiff'])

su_means = conts[(conts['subblock'] == 'aus+sua')].groupby('ID')['RTdiff'].mean()
su_std = conts[(conts['subblock'] == 'aus+sua')].groupby('ID')['RTdiff'].aggregate(sem)
su_t_means = conts[(conts['subblock'] == 'aus+sua')]['RTdiff'].mean()
su_t_std = sem(conts[(conts['subblock'] == 'aus+sua')]['RTdiff'])

if isspec:
	sa_spec_means = spec_conts[(spec_conts['subblock'] == 'uas+sau')]['RTdiff'].mean()
	sa_spec_std = sem(spec_conts[(spec_conts['subblock'] == 'uas+sau')]['RTdiff'])

	su_spec_means = spec_conts[(spec_conts['subblock'] == 'aus+sua')]['RTdiff'].mean()
	su_spec_std = sem(spec_conts[(spec_conts['subblock'] == 'aus+sua')]['RTdiff'])

fig = figure(figsize=(pos_ids.max(), 6), dpi=80,facecolor='#eeeeee', tight_layout=True)
ax=fig.add_subplot(1,1,1)
width = 0.3
ax.yaxis.grid(True, linestyle='-', which='major', color='#dddddd',alpha=0.5, zorder = 1)
#box_plots = plt.boxplot(sa_li)
#box_plots = plt.boxplot(su_li)

sa_bar = plt.bar(pos_ids, sa_means, width ,color='m', alpha=0.4, zorder = 1)
sa_err = errorbar(pos_ids+(width/2), sa_means, yerr=sa_std, ecolor='0.5', elinewidth='3', capsize=0, linestyle='None', zorder = 2)
sa_t_bar = plt.bar(pos_ids[-1]+1, sa_t_means, width ,color='m', alpha=0.8, zorder = 1)
sa_t_err = errorbar(pos_ids[-1]+1+(width/2), sa_t_means, yerr=sa_t_std, ecolor='0.1', elinewidth='3', capsize=0, linestyle='None', zorder = 2)

su_bar = plt.bar(pos_ids+width, su_means, width ,color='g', alpha=0.4, zorder = 1)
su_err = errorbar(pos_ids+(width*3/2), su_means, yerr=su_std, ecolor='0.5', elinewidth='3', capsize=0, linestyle='None', zorder = 2)
su_t_bar = plt.bar(pos_ids[-1]+1+width, su_t_means, width ,color='g', alpha=0.8, zorder = 1)
su_t_err = errorbar(pos_ids[-1]+1+(width*3/2), su_t_means, yerr=su_t_std, ecolor='0.1', elinewidth='3', capsize=0, linestyle='None', zorder = 2)

if isspec:
	sa_spec_bar = plt.bar(pos_ids[-1]+2, sa_spec_means, width ,color='m', alpha=0.4, zorder = 1)
	sa_spec_err = errorbar(pos_ids[-1]+2+(width*1/2), sa_spec_means, yerr=sa_spec_std, ecolor='0.5', elinewidth='3', capsize=0, linestyle='None', zorder = 2)
	su_spec_bar = plt.bar(pos_ids[-1]+2+width, su_spec_means, width ,color='g', alpha=0.4, zorder = 1)
	su_spec_err = errorbar(pos_ids[-1]+2+(width*3/2), su_spec_means, yerr=su_spec_std, ecolor='0.5', elinewidth='3', capsize=0, linestyle='None', zorder = 2)

if isspec:
	ids=ids+['total',spec]
else:ids=ids+['total']
pos_ids = np.arange(len(ids))
ax.set_xlim(0, pos_ids.max())
ax.set_ylabel(r'$\mathsf{RT - \overline{RT}_{aa;uu}}$ [s]', fontsize=13)
ax.set_xlabel('Participant ID')
ax.set_xticks(pos_ids + width)
ax.set_xticklabels(ids,fontsize=9, rotation=30)
#setp(ax.set_xticklabels, 'rotation', 'vertical')
for tick in ax.axes.get_xticklines():
	tick.set_visible(False)
axis.Axis.zoom(ax.xaxis, -0.5)
legend((sa_t_bar,su_t_bar),('Stimulus flanking attracive face','Stimulus flanking unattractive face'), 'lower right', shadow=False, frameon=False, prop= FontProperties(size='11'))
show()
