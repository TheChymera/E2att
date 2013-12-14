#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
from os import listdir, path
from lefunctions import get_scatterdata
from scipy.stats import ttest_ind, pearsonr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
from matplotlib.font_manager import FontProperties
from pylab import figure, show, errorbar, setp, legend
from matplotlib import axis

globalpath = '~/data/2att/' #root of results
bh_results = 'bh/' # behavioural test results
cq_results = 'cq/' # questionnaire results

globalpath = path.expanduser(globalpath)
bhpath = globalpath + bh_results
cqpath = globalpath + cq_results

files = [lefile for lefile in listdir(bhpath) if lefile.endswith('.csv')]
ids = [t.split('_',2)[0]+'_'+t.split('_',2)[1] for t in files]
ids = np.unique(ids)
spec = ['6245247_f']
h_dist = ['1236345_f','3292380_m','6779353_f','7310001_f','7714775_m','7816097_m','7865828_m','7922847_m']
l_dist = ['1975801_m','4724273_f','6268973_m','8963557_f','8286497_m','8963557_m','9651558_m','8240877_m','6887665_m','5559429_f','8582941_f','8582941_m','9302438_f','4276763_f','3878418_m','3537898_f','1247497_f','8717741_m','4744495_f','7117377_m']
test = ['chr1_f','chr2_f']

id_list = l_dist
isspec=False

conts = get_scatterdata(id_list,bhpath)
if isspec: 
	spec_conts = get_scatterdata(spec,bhpath)
	print pearsonr(spec_conts['ratediff'], spec_conts['RTdiff'])

print pearsonr(conts['ratediff'], conts['RTdiff'])

fig = figure(dpi=80,facecolor='#eeeeee', tight_layout=True)
ax=fig.add_subplot(1,1,1)
width = 0.3
ax.yaxis.grid(True, linestyle='-', which='major', color='#dddddd',alpha=0.5, zorder = 1)
if isspec:
	ax.plot(conts['RTdiff'], conts['ratediff'], '.', markersize=8, markeredgecolor='#7ECC5A', markerfacecolor='#7ECC5A', alpha=0.5, zorder=1)
	A = np.vstack([conts['RTdiff'], np.ones(len(conts['RTdiff']))]).T
	m, c = np.linalg.lstsq(A, conts['ratediff'])[0]
	plt.plot(conts['RTdiff'],conts['RTdiff']*m+c,color='#7ECC5A', antialiased=True)
	ax.plot(spec_conts['RTdiff'], spec_conts['ratediff'], '.', markersize=8, markeredgecolor='m',markerfacecolor='m', zorder=2)
	s_A = np.vstack([spec_conts['RTdiff'], np.ones(len(spec_conts['RTdiff']))]).T
	s_m, s_c = np.linalg.lstsq(s_A, spec_conts['ratediff'])[0]
	plt.plot(spec_conts['RTdiff'],spec_conts['RTdiff']*s_m+s_c,color='m',antialiased=True)
else: 
	ax.plot(conts['RTdiff'], conts['ratediff'], '.', markersize=8, markeredgecolor='#7ECC5A', markerfacecolor='#7ECC5A', alpha=1, zorder=1)
	A = np.vstack([conts['RTdiff'], np.ones(len(conts['RTdiff']))]).T
	m, c = np.linalg.lstsq(A, conts['ratediff'])[0]
	plt.plot(conts['RTdiff'],conts['RTdiff']*m+c,color='#7ECC5A', antialiased=True)
ax.set_ylabel('Rating difference (stimulus side - distractor side)')
ax.set_xlabel(r'$\mathsf{RT - \overline{RT}_{aa;uu}}$ [s]', fontsize=13)
plt.show()
