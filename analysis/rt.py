#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
from os import listdir, path
from lefunctions import get_scatterdata, get_dataframes, open_csv
from scipy.stats import sem
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
from matplotlib.font_manager import FontProperties
from pylab import figure, show, errorbar, setp, legend
from matplotlib import axis
import matplotlib
from chr_helpers import get_config_file

spec = ['6245247_f']
h_dist = ['1236345_f','6779353_f','7310001_f','7714775_m','7816097_m','7865828_m','7922847_m']
l_dist = ['1975801_m','4724273_f','6268973_m','8963557_f','8286497_m','8963557_m','9651558_m','8240877_m','6887665_m','5559429_f','8582941_f','8582941_m','9302438_f','4276763_f','3878418_m','3537898_f','1247497_f','8717741_m','4744495_f','7117377_m']
test = ['chr1_f','chr2_f']
id_list = l_dist

def corr(source=False, num_bins=False, keep_scrambling=False, make_tight=True, print_title = True, linewidth=0.5, fontscale=1):
    config = get_config_file(localpath=path.dirname(path.realpath(__file__))+'/')
	    
    #IMPORT VARIABLES
    if not source:
	    source = config.get('Source', 'source')
    data_path = config.get('Addresses', source)
    reaction_times = config.get('Addresses', 'reaction_times')
    #END IMPORT VARIABLES
    
    data_path = path.expanduser(data_path)
    rt_path = data_path + reaction_times
    
    files = [lefile for lefile in listdir(rt_path) if lefile.endswith('.csv')]
    ids = [t.split('_',2)[0]+'_'+t.split('_',2)[1] for t in files]
    ids = np.unique(ids)
    id_list = l_dist
    isspec=False
    
    conts = get_scatterdata(id_list,rt_path)
    if isspec: 
	spec_conts = get_scatterdata(spec,rt_path)
	print pearsonr(spec_conts['ratediff'], spec_conts['RTdiff'])
    
    print pearsonr(conts['ratediff'], conts['RTdiff'])
    
    fig = figure(dpi=80,facecolor='#eeeeee', tight_layout=True)
    ax=fig.add_subplot(1,1,1)
    width = 0.3
    ax.yaxis.grid(True, linestyle='-', which='major', color='#dddddd',alpha=0.5, zorder = 1)
    if isspec:
	ax.plot(conts['RTdiff'], conts['ratediff'], 'o', markersize=3, markeredgecolor='#7ECC5A', markerfacecolor='#7ECC5A', alpha=0.5, zorder=1)
	A = np.vstack([conts['RTdiff'], np.ones(len(conts['RTdiff']))]).T
	m, c = np.linalg.lstsq(A, conts['ratediff'])[0]
	plt.plot(conts['RTdiff'],conts['RTdiff']*m+c,color='#7ECC5A', antialiased=True)
	ax.plot(spec_conts['RTdiff'], spec_conts['ratediff'], '.', markersize=8, markeredgecolor='m',markerfacecolor='m', zorder=2)
	s_A = np.vstack([spec_conts['RTdiff'], np.ones(len(spec_conts['RTdiff']))]).T
	s_m, s_c = np.linalg.lstsq(s_A, spec_conts['ratediff'])[0]
	plt.plot(spec_conts['RTdiff'],spec_conts['RTdiff']*s_m+s_c,color='m',antialiased=True)
    else: 
	ax.plot(conts['RTdiff'], conts['ratediff'], 'o', markersize=3, markeredgecolor='#7ECC5A', markerfacecolor='#7ECC5A', alpha=0.5, zorder=1)
	A = np.vstack([conts['RTdiff'], np.ones(len(conts['RTdiff']))]).T
	m, c = np.linalg.lstsq(A, conts['ratediff'])[0]
	plt.plot(conts['RTdiff'],conts['RTdiff']*m+c,color='#7ECC5A', antialiased=True)
    ax.set_ylabel('Rating difference (stimulus side - distractor side)')
    ax.set_xlabel(r'$\mathsf{RT - \overline{RT}_{aa;uu}}$ [s]', fontsize=13)
    return m, c
    
	
# this function creates bar plots for participants and for the total in the categories of interest (coi)
def coi(source=False, make_tight=True, print_title = True, elinewidth=3, fontscale=1, isspec = False):
    config = get_config_file(localpath=path.dirname(path.realpath(__file__))+'/')
	    
    #IMPORT VARIABLES
    if not source:
	    source = config.get('Source', 'source')
    data_path = config.get('Addresses', source)
    reaction_times = config.get('Addresses', 'reaction_times')
    #END IMPORT VARIABLES
    
    data_path = path.expanduser(data_path)
    rt_path = data_path + reaction_times
    
    files = [lefile for lefile in listdir(rt_path) if lefile.endswith('.csv')]
    ids = [t.split('_',2)[0]+'_'+t.split('_',2)[1] for t in files]
    ids = np.unique(ids)
    
    conts = get_dataframes(id_list, rt_path)
    if isspec: 
	spec_conts = get_dataframes(spec, rt_path)
	meanscont = spec_conts.groupby('subblock').mean()
	print meanscont
	cat1 = spec_conts[spec_conts['subblock']=='aus+sua']
	cat2 = spec_conts[spec_conts['subblock']=='uas+sau']
	print ttest_rel(cat1['RTdiff'], cat2['RTdiff'])
    
    meanscont = conts.groupby(['ID','subblock']).mean()
    meanscont = meanscont.reset_index()
    
    ids = sorted(list(set(conts.set_index('ID').index)))
    pos_ids = np.arange(len(ids))
    
    sa_means = conts[(conts['subblock'] == 'uas+sau')].groupby('ID')['RTdiff'].mean()
    sa_std = conts[(conts['subblock'] == 'uas+sau')].groupby('ID')['RTdiff'].aggregate(sem)
    
    su_means = conts[(conts['subblock'] == 'aus+sua')].groupby('ID')['RTdiff'].mean()
    su_std = conts[(conts['subblock'] == 'aus+sua')].groupby('ID')['RTdiff'].aggregate(sem)
    
    sa_means = conts[(conts['subblock'] == 'uas+sau')].groupby('ID')['RTdiff'].mean()
    sa_std = conts[(conts['subblock'] == 'uas+sau')].groupby('ID')['RTdiff'].aggregate(sem)
    sa_t_means = meanscont[(meanscont['subblock'] == 'uas+sau')]['RTdiff'].mean()
    sa_t_std = sem(meanscont[(meanscont['subblock'] == 'uas+sau')]['RTdiff'])
    
    su_means = conts[(conts['subblock'] == 'aus+sua')].groupby('ID')['RTdiff'].mean()
    su_std = conts[(conts['subblock'] == 'aus+sua')].groupby('ID')['RTdiff'].aggregate(sem)
    su_t_means = meanscont[(meanscont['subblock'] == 'aus+sua')]['RTdiff'].mean()
    su_t_std = sem(meanscont[(meanscont['subblock'] == 'aus+sua')]['RTdiff'])
    
    if isspec:
	sa_spec_means = spec_conts[(spec_conts['subblock'] == 'uas+sau')]['RTdiff'].mean()
	sa_spec_std = sem(spec_conts[(spec_conts['subblock'] == 'uas+sau')]['RTdiff'])
	
	su_spec_means = spec_conts[(spec_conts['subblock'] == 'aus+sua')]['RTdiff'].mean()
	su_spec_std = sem(spec_conts[(spec_conts['subblock'] == 'aus+sua')]['RTdiff'])
    
    fig = figure(figsize=(pos_ids.max()*3, 4), dpi=300, facecolor='#eeeeee', tight_layout=make_tight)
    ax=fig.add_subplot(1,1,1)
    matplotlib.rcParams.update({'font.size': 12*fontscale})
    width = 0.3
    ax.yaxis.grid(True, linestyle='-', which='major', color='#dddddd',alpha=0.5, zorder=1)
    
    sa_bar = plt.bar(pos_ids, sa_means, width ,color='m', alpha=0.4, zorder=1, linewidth=0)
    sa_err = errorbar(pos_ids+(width/2), sa_means, yerr=sa_std, ecolor='0.55', elinewidth=elinewidth, capsize=0, linestyle='None', zorder=2)
    sa_t_bar = plt.bar(pos_ids[-1]+1, sa_t_means, width ,color='m', alpha=0.8, zorder=1, linewidth=0)
    sa_t_err = errorbar(pos_ids[-1]+1+(width/2), sa_t_means, yerr=sa_t_std, ecolor='0.1', elinewidth=elinewidth, capsize=0, linestyle='None', zorder=2)
    
    su_bar = plt.bar(pos_ids+width, su_means, width ,color='g', alpha=0.4, zorder=1, linewidth=0)
    su_err = errorbar(pos_ids+(width*3/2), su_means, yerr=su_std, ecolor='0.55', elinewidth=elinewidth, capsize=0, linestyle='None', zorder=2)
    su_t_bar = plt.bar(pos_ids[-1]+1+width, su_t_means, width ,color='g', alpha=0.8, zorder=1, linewidth=0)
    su_t_err = errorbar(pos_ids[-1]+1+(width*3/2), su_t_means, yerr=su_t_std, ecolor='0.1', elinewidth=elinewidth, capsize=0, linestyle='None', zorder=2)
    
    if isspec:
	sa_spec_bar = plt.bar(pos_ids[-1]+2, sa_spec_means, width ,color='m', alpha=0.4, zorder=1, linewidth=0)
	sa_spec_err = errorbar(pos_ids[-1]+2+(width*1/2), sa_spec_means, yerr=sa_spec_std, ecolor='0.55', elinewidth=elinewidth, capsize=0, linestyle='None', zorder=2)
	su_spec_bar = plt.bar(pos_ids[-1]+2+width, su_spec_means, width ,color='g', alpha=0.4, zorder=1, linewidth=0)
	su_spec_err = errorbar(pos_ids[-1]+2+(width*3/2), su_spec_means, yerr=su_spec_std, ecolor='0.55', elinewidth=elinewidth, capsize=0, linestyle='None', zorder=2)
    
    if isspec:
	ids=ids+['total',spec]
    else:
	ids=ids+['TOTAL  '] # blank space at the end so that it doesn't overlap with the x-axis
    pos_ids = np.arange(len(ids))
    ax.set_xlim(0, pos_ids.max())
    ax.set_ylabel(r'$\mathsf{\overline{RT}}$ [s]')
    ax.set_xlabel('Participant ID')
    ax.set_xticks(pos_ids + width)
    ax.set_xticklabels(ids,fontsize=8*fontscale,rotation=90)
    for tick in ax.axes.get_xticklines():
	tick.set_visible(False)
    axis.Axis.zoom(ax.xaxis, -0.5)
    legend((sa_t_bar,su_t_bar),('Target flanking attracive face','Target flanking unattractive face'), bbox_to_anchor=(0.92, 0.2), shadow=False, frameon=False, prop=FontProperties(size=str(11*fontscale)))
    print meanscont[meanscont['subblock']=='uas+sau']['RTdiff'].mean()-meanscont[meanscont['subblock']=='aus+sua']['RTdiff'].mean()
    return meanscont


# this function creates bar plots for participants and for the total in the categories of no interest (coni)
def coni(source=False, make_tight=True, print_title = True, elinewidth=2, fontscale=1, isspec = False):
    config = get_config_file(localpath=path.dirname(path.realpath(__file__))+'/')
	    
    #IMPORT VARIABLES
    if not source:
	    source = config.get('Source', 'source')
    data_path = config.get('Addresses', source)
    reaction_times = config.get('Addresses', 'reaction_times')
    #END IMPORT VARIABLES
    
    data_path = path.expanduser(data_path)
    rt_path = data_path + reaction_times
    
    files = [lefile for lefile in listdir(rt_path) if lefile.endswith('.csv')]
    ids = [t.split('_',2)[0]+'_'+t.split('_',2)[1] for t in files]
    ids = np.unique(ids)
    conts = pd.DataFrame([])
    
    for i in id_list:
	ratings = open_csv(rt_path+i+'_p')
	ratings = pd.DataFrame(ratings[1:], columns=ratings[0], dtype=float)
	ratings = ratings.groupby('picture').mean()    
	sorted_scores = sorted(ratings['score'])
	score_top, score_bottom = sorted_scores[-20], sorted_scores	[19]

	cont = open_csv(rt_path+i+'_wm')
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
    
    meanscont = conts.groupby(['ID','block']).mean()
    meanscont = meanscont.reset_index()
    
    aa_means = conts[(conts['block'] == 'aa')].groupby('ID')['RT'].mean()
    aa_std = conts[(conts['block'] == 'aa')].groupby('ID')['RT'].aggregate(sem)
    aa_t_means = meanscont[(meanscont['block'] == 'aa')]['RT'].mean()
    aa_t_std = sem(meanscont[(meanscont['block'] == 'aa')]['RT'])
    
    uu_means = conts[(conts['block'] == 'uu')].groupby('ID')['RT'].mean()
    uu_std = conts[(conts['block'] == 'uu')].groupby('ID')['RT'].aggregate(sem)
    uu_t_means = meanscont[(meanscont['block'] == 'uu')]['RT'].mean()
    uu_t_std = sem(meanscont[(meanscont['block'] == 'uu')]['RT'])
    
    fig = figure(figsize=(pos_ids.max()*3, 4), dpi=300, facecolor='#eeeeee', tight_layout=make_tight)
    ax=fig.add_subplot(1,1,1)
    matplotlib.rcParams.update({'font.size': 12*fontscale})
    width = 0.3
    ax.yaxis.grid(True, linestyle='-', which='major', color='#dddddd',alpha=0.5, zorder=1)
    
    aa_bar = plt.bar(pos_ids, aa_means, width ,color='g', alpha=0.4, zorder=1, linewidth=0)
    aa_err = errorbar(pos_ids+(width/2), aa_means, yerr=aa_std, ecolor='0.55', elinewidth=elinewidth, capsize=0, linestyle='None', zorder=2)
    aa_t_bar = plt.bar(pos_ids[-1]+1, aa_t_means, width ,color='g', alpha=0.8, zorder=1, linewidth=0)
    aa_err = errorbar(pos_ids[-1]+1+(width/2), aa_t_means, yerr=aa_t_std, ecolor='0.1', elinewidth=elinewidth, capsize=0, linestyle='None', zorder=2)
    
    uu_bar = plt.bar(pos_ids+width, uu_means, width ,color='m', alpha=0.4, zorder=1, linewidth=0)
    uu_err = errorbar(pos_ids+(width*3/2), uu_means, yerr=uu_std, ecolor='0.55', elinewidth=elinewidth, capsize=0, linestyle='None', zorder=2)
    uu_t_bar = plt.bar(pos_ids[-1]+1+width, uu_t_means, width ,color='m', alpha=0.8, zorder=1, linewidth=0)
    uu_err = errorbar(pos_ids[-1]+1+(width*3/2), uu_t_means, yerr=uu_t_std, ecolor='0.1', elinewidth=elinewidth, capsize=0, linestyle='None', zorder=2)
    
    ids=ids+['TOTAL  '] # blank space at the end so that it doesn't overlap with the x-axis
    pos_ids = np.arange(len(ids))
    ax.set_xlim(0, pos_ids.max())
    ax.set_ylim(0, 1.1)
    ax.set_ylabel(r'$\mathsf{\overline{RT}}$ [s]')
    ax.set_xlabel('Participant ID')
    ax.set_xticks(pos_ids + width)
    ax.set_xticklabels(ids,fontsize=8*fontscale,rotation=90)
    for tick in ax.axes.get_xticklines():
	tick.set_visible(False)
    axis.Axis.zoom(ax.xaxis, -0.5)
    legend((aa_t_bar,uu_t_bar),('Only attractive faces','Only unattractive faces'), bbox_to_anchor=(0.92, 1), shadow=False, frameon=False, prop=FontProperties(size=str(11*fontscale)))
    return meanscont

if __name__ == '__main__':
    coi()
    show()
