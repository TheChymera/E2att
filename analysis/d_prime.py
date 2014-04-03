#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
from os import listdir, path
from lefunctions import get_dataframes_for_dp
from scipy.stats import ttest_ind, norm, sem, f_oneway
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import axis
from matplotlib.font_manager import FontProperties
from pylab import figure, show, errorbar, setp, legend
#from statsmodels.stats.anova import anova_lm

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
isspec=False

t_cr_au,t_fa_au,t_ht_au,t_ms_au,t_cr_aa,t_fa_aa,t_ht_aa,t_ms_aa,t_cr_uu,t_fa_uu,t_ht_uu,t_ms_uu,all_au_dp,all_aa_dp,all_uu_dp = get_dataframes_for_dp(id_list, bhpath)
if isspec:
	_,_,_,_,_,_,_,_,_,_,_,_,s_dp_au,s_dp_aa,s_dp_uu = get_dataframes_for_dp(spec, bhpath)

t_hr_au = t_ht_au / (t_ht_au+t_ms_au)
t_far_au = t_fa_au / (t_cr_au+t_fa_au)
t_zhr_au = norm.ppf(t_hr_au)
t_zfar_au = norm.ppf(t_far_au)
t_dp_au = t_zhr_au-t_zfar_au

t_hr_aa = t_ht_aa / (t_ht_aa+t_ms_aa)
t_far_aa = t_fa_aa / (t_cr_aa+t_fa_aa)
t_zhr_aa = norm.ppf(t_hr_aa)
t_zfar_aa = norm.ppf(t_far_aa)
t_dp_aa = t_zhr_aa-t_zfar_aa

t_hr_uu = t_ht_uu / (t_ht_uu+t_ms_uu)
t_far_uu = t_fa_uu / (t_cr_uu+t_fa_uu)
t_zhr_uu = norm.ppf(t_hr_uu)
t_zfar_uu = norm.ppf(t_far_uu)
t_dp_uu = t_zhr_uu-t_zfar_uu

ids = sorted(id_list)
pos_ids = np.arange(len(ids))

fig = figure(figsize=(pos_ids.max(), 5), dpi=80,facecolor='#eeeeee',tight_layout=True)
ax=fig.add_subplot(1,1,1)
width = 0.7
ax.yaxis.grid(True, linestyle='-', which='major', color='#dddddd',alpha=0.5, zorder = 1)

au_bars = plt.bar(pos_ids, all_au_dp, width/3 ,color='m', alpha=0.4, zorder = 1)
aa_bars = plt.bar(pos_ids+width/3, all_aa_dp, width/3 ,color='#488C0F', alpha=0.4, zorder = 1)
uu_bars = plt.bar(pos_ids+width*2/3, all_uu_dp, width/3 ,color='#0F8C2F', alpha=0.4, zorder = 1)

au_t_bar = plt.bar(pos_ids[-1]+1, np.mean(all_au_dp), width/3 ,color='m', alpha=0.8, zorder = 1)
au_t_err = errorbar(pos_ids[-1]+1+(width/6), np.mean(all_au_dp), yerr=sem(all_au_dp), ecolor='0.1', elinewidth='3', capsize=0, linestyle='None', zorder = 2)
aa_t_bar = plt.bar(pos_ids[-1]+1+width/3, np.mean(all_aa_dp), width/3 ,color='#488C0F', alpha=0.8, zorder = 1)
aa_t_err = errorbar(pos_ids[-1]+1+(width*3/6), np.mean(all_aa_dp), yerr=sem(all_aa_dp), ecolor='0.1', elinewidth='3', capsize=0, linestyle='None', zorder = 2)
uu_t_bar = plt.bar(pos_ids[-1]+1+width*2/3, np.mean(all_uu_dp), width/3,color='#0F8C2F', alpha=0.8, zorder = 1)
uu_t_err = errorbar(pos_ids[-1]+1+(width*5/6), np.mean(all_uu_dp), yerr=sem(all_uu_dp), ecolor='0.1', elinewidth='3', capsize=0, linestyle='None', zorder = 2)

if isspec:
	s_au_bars = plt.bar(pos_ids[-1]+2, s_dp_au, width/3 ,color='m', alpha=0.4, zorder = 1)
	s_aa_bars = plt.bar(pos_ids[-1]+2+width/3, s_dp_aa, width/3 ,color='#488C0F', alpha=0.4, zorder = 1)
	s_uu_bars = plt.bar(pos_ids[-1]+2+width*2/3, s_dp_uu, width/3 ,color='#0F8C2F', alpha=0.4, zorder = 1)

print f_oneway(all_au_dp,all_aa_dp,all_uu_dp)

if isspec:
	ids=ids+['total',spec]
else:ids=ids+['total']
pos_ids = np.arange(len(ids))
ax.set_xlim(0, pos_ids.max()+0.7)
ax.set_ylim(0,9)
ax.set_ylabel('Sensitivity Index (d\')')
ax.set_xlabel('Participant ID')
ax.set_xticks(pos_ids + width/2)
ax.set_xticklabels(ids,fontsize=9,rotation=30)
#setp(ax.set_xticklabels, 'rotation', 'vertical')
for tick in ax.axes.get_xticklines():
	tick.set_visible(False)
axis.Axis.zoom(ax.xaxis, -0.3)
legend((au_t_bar,aa_t_bar,uu_t_bar),('Mixed faces','Attractive faces only','Unattractive faces only'), 'upper right', shadow=False, frameon=False, prop= FontProperties(size='11'))
show()
