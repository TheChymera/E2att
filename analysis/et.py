#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
from os import listdir, path
from lefunctions import open_csv, get_dataframes
from scipy.stats import ttest_ind, sem
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.font_manager import FontProperties
from pylab import figure, show, errorbar, setp, legend
from matplotlib import axis
from chr_helpers import get_config_file

# this function does a "total", time resolved analysis of gaze coordinates along one axis 
def ett(plot_axis="x", source=False, id_list="final", make_tight=True, print_title = True, linewidth=0.8, fontscale=0.5, isspec = False):
    config = get_config_file(localpath=path.dirname(path.realpath(__file__))+'/')
	    
    #IMPORT VARIABLES
    if not source:
	    source = config.get('Source', 'source')
    data_path = config.get('Addresses', source)
    reaction_times = config.get('Addresses', 'reaction_times')
    #END IMPORT VARIABLES
    
    if plot_axis == "x":
	plot_axis = 'GazePointX'
    if plot_axis == "y":
	plot_axis = 'GazePointY'
    data_path = path.expanduser(data_path)
    rt_path = data_path + reaction_times
    
    files = [lefile for lefile in listdir(rt_path) if lefile.endswith('.tsv')]
    ids = [t.split('_',2)[0]+'_'+t.split('_',2)[1] for t in files]
    ids = np.unique(ids)
    eye_data_total = pd.DataFrame([])
    stimulus_datas = pd.DataFrame([])
    spec = ['6245247_f']
    h_dist = ['1236345_f','6779353_f','7310001_f','7714775_m','7816097_m','7865828_m','7922847_m']
    l_dist = ['1975801_m','4724273_f','6268973_m','8963557_f','8286497_m','8963557_m','9651558_m','8240877_m','6887665_m','5559429_f','8582941_f','8582941_m','9302438_f','4276763_f','3878418_m','3537898_f','1247497_f','8717741_m','4744495_f','7117377_m']
    best = ['1975801_m','4724273_f','6268973_m','8963557_f','8286497_m','8963557_m','6887665_m','5559429_f','8582941_f','9302438_f','1247497_f','4744495_f','7117377_m']
    test = ['chr1_f','chr2_f']
    if id_list=="final":
	id_list = l_dist
    
    for fileidx, fileid in enumerate(id_list):
	ratings = open_csv(rt_path+fileid+'_p')
	ratings = pd.DataFrame(ratings[1:], columns=ratings[0], dtype=float)
	ratings = ratings.groupby('picture').mean()    
	sorted_scores = sorted(ratings['score'])
	score_top, score_bottom = sorted_scores[-20], sorted_scores	[19]
	
	stimulus_data = pd.DataFrame
	stimulus_data = stimulus_data.from_csv(rt_path+fileid+'_wm.csv')
	stimulus_data['rateL'] = stimulus_data['rateL'].astype(np.float64)
	stimulus_data['RTL'] = stimulus_data['RTL'].astype(np.float64)
	stimulus_data['orderL'] = stimulus_data['orderL'].astype(np.float64)
	stimulus_data['rateR'] = stimulus_data['rateR'].astype(np.float64)
	stimulus_data['RTR'] = stimulus_data['RTR'].astype(np.float64)
	stimulus_data['orderR'] = stimulus_data['orderR'].astype(np.float64)
	stimulus_data['RT'] = stimulus_data['RT'].astype(np.float64)
	stimulus_data['session'] = stimulus_data['session'].astype(np.float64)
	stimulus_data = stimulus_data[stimulus_data['RT'] >=0]
	stimulus_data['block'] = ''
	stimulus_data.ix[(stimulus_data['rateL'] >= score_top) & (stimulus_data['rateR'] >= score_top), 'block'] = 'aa'
	stimulus_data.ix[(stimulus_data['rateL'] >= score_top) & (stimulus_data['rateR'] <= score_bottom), 'block'] = 'au'
	stimulus_data.ix[(stimulus_data['rateL'] <= score_bottom) & (stimulus_data['rateR'] >= score_top), 'block'] = 'ua'
	stimulus_data.ix[(stimulus_data['rateL'] <= score_bottom) & (stimulus_data['rateR'] <= score_bottom), 'block'] = 'uu'
	
	aa_trials = list(stimulus_data[(stimulus_data['block'] == 'aa')]['session'])
	au_trials = list(stimulus_data[(stimulus_data['block'] == 'au')]['session'])
	ua_trials = list(stimulus_data[(stimulus_data['block'] == 'ua')]['session'])
	uu_trials = list(stimulus_data[(stimulus_data['block'] == 'uu')]['session'])
	
	stimleft_trials = list(stimulus_data[(stimulus_data['isstimleft'] == True)]['session'])
	stimright_trials = list(stimulus_data[(stimulus_data['isstimleft'] == False)]['session'])
	stimatt_trials = list(stimulus_data[(stimulus_data['isstimleft'] == True) & (stimulus_data['rateL'] >= score_top) & (stimulus_data['rateR'] <= score_bottom)]['session'])
	stimatt_trials = stimatt_trials + list(stimulus_data[(stimulus_data['isstimleft'] == False) & (stimulus_data['rateL'] <= score_bottom) & (stimulus_data['rateR'] >= score_top)]['session'])
	stimNatt_trials = list(stimulus_data[(stimulus_data['isstimleft'] == False) & (stimulus_data['rateL'] >= score_top) & (stimulus_data['rateR'] <= score_bottom)]['session'])
	stimNatt_trials = stimNatt_trials + list(stimulus_data[(stimulus_data['isstimleft'] == True) & (stimulus_data['rateL'] <= score_bottom) & (stimulus_data['rateR'] >= score_top)]['session'])
	
	pat = 'TimeStamp	GazePointXLeft	GazePointYLeft	ValidityLeft	GazePointXRight	GazePointYRight	ValidityRight	GazePointX	GazePointY	Event'
	with open(rt_path+fileid+'_wmet.tsv') as infile:
	    eye_data = infile.read().split(pat)
	    eye_data = eye_data[1:] # remove header (describing date etc)
	    eye_data = [trial.split('\r\n') for trial in eye_data] # split at '\r'
	    for idx, i in enumerate(eye_data): # crop to 447 ACTUAL time frames - the first one is empty
		eye_data[idx] = i[:448]
	    for idx, trial in enumerate(eye_data):
		trial = [row.split('\t') for row in trial]
		eye_data[idx] = trial
	    eye_data = [name[1:] for name in eye_data] # crop the first, empty line
    
	    eye_data = np.array(eye_data)
	    eye_data = eye_data[:,:,[0,3,6,7,8]].astype(np.float64) # convert to float, we don't need separate eye coordinates
	    eye_data[:,:,3:] = eye_data[:,:,3:] / 2 - 0.5 # the integrated left-right gaze coordinates are the sum of the per-eye screen percentages - divide by 2 (2 eyes) and normalize to: 50% = 0
    
	    for a in np.arange(np.shape(eye_data)[0]): # assume that when neither of the eyes is detected the subject looks at the fixation
		for i in np.arange(np.shape(eye_data)[1]):
		    if eye_data[a,i,1] == 4 and eye_data[a,i,2] == 4:
			eye_data[a,i,3] = 0
			eye_data[a,i,4] = 0
    
	for i in stimleft_trials: # invert stimleft trial coordinates - equates 'right' with 'stimside'
	    eye_data[i,:,3:] = -eye_data[i,:,3:]
	eye_data = eye_data[:,:,[0,3,4]]  # we can't work with eye detection indices in the subsequent sumation, discard them here
	eye_data_aa = eye_data[aa_trials,:,:]
	eye_data_uu = eye_data[uu_trials,:,:]
	eye_data_uas = eye_data[stimatt_trials,:,:]
	eye_data_aus = eye_data[stimNatt_trials,:,:]
    
	eye_data_aa = np.sum(eye_data_aa, axis=0) / np.shape(eye_data_aa)[0]
	eye_data_uu = np.sum(eye_data_uu, axis=0) / np.shape(eye_data_uu)[0]
	eye_data_uas = np.sum(eye_data_uas, axis=0) / np.shape(eye_data_uas)[0]
	eye_data_aus = np.sum(eye_data_aus, axis=0) / np.shape(eye_data_aus)[0]
	
	eye_data_aa = pd.DataFrame(eye_data_aa, columns=['time','GazePointX','GazePointY'])
	eye_data_aa['stimuli'] = 'aa' 
	eye_data_uu = pd.DataFrame(eye_data_uu, columns=['time','GazePointX','GazePointY'])
	eye_data_uu['stimuli'] = 'uu' 
	eye_data_uas = pd.DataFrame(eye_data_uas, columns=['time','GazePointX','GazePointY'])
	eye_data_uas['stimuli'] = 'uas'
	eye_data_aus = pd.DataFrame(eye_data_aus, columns=['time','GazePointX','GazePointY'])
	eye_data_aus['stimuli'] = 'aus'
    
	eye_data = pd.concat([eye_data_aa, eye_data_uu, eye_data_uas, eye_data_aus])
	eye_data['ID'] = fileid
	if fileidx == 0:
	    eye_data_total = eye_data[['time','GazePointX','GazePointY','stimuli']]
	else:
	    eye_data_total[['time','GazePointX','GazePointY']] = eye_data_total[['time','GazePointX','GazePointY']] + eye_data[['time','GazePointX','GazePointY']]
    
    # load reaction times (to plot as lines) here:
    conts = get_dataframes(id_list, rt_path)
    sa_reaction_time = conts[(conts['subblock'] == 'uas+sau')]['RT'].mean()*1000
    su_reaction_time = conts[(conts['subblock'] == 'aus+sua')]['RT'].mean()*1000
    aa_reaction_time = conts[(conts['block'] == 'aa')]['RT'].mean()*1000
    uu_reaction_time = conts[(conts['block'] == 'uu')]['RT'].mean()*1000
    # end load reaction times
    
    eye_data_total[['time','GazePointX','GazePointY']] = eye_data_total[['time','GazePointX','GazePointY']] / len(id_list)
    
    fig = figure(figsize=(3, 4), dpi=300, facecolor='#eeeeee', tight_layout=make_tight)
    ax1=fig.add_subplot(2,1,1)
    matplotlib.rcParams.update({'font.size': 12*fontscale})
    
    ax1.set_xlim(0, eye_data_total['time'].max())
    ax1.plot(eye_data_total[(eye_data_total['stimuli'] == 'aa')]['time'],eye_data_total[(eye_data_total['stimuli'] == 'aa')][plot_axis], color='g')
    ax1.plot(eye_data_total[(eye_data_total['stimuli'] == 'uu')]['time'],eye_data_total[(eye_data_total['stimuli'] == 'uu')][plot_axis], color='m')
    legend(('Attractive - Attractive','Unattractive - Unattractive'), bbox_to_anchor=(0.93, 1), shadow=False, frameon=False, prop=FontProperties(size=str(9*fontscale)))
    ax1.axhline(0, color='k', alpha = 0.1, linewidth=linewidth)
    ax1.axvline(aa_reaction_time, color='g', alpha = 0.3, linewidth=linewidth)
    ax1.axvline(uu_reaction_time, color='m', alpha = 0.3, linewidth=linewidth)
    ax1.set_ylabel('X-axis % (towards stimulus)')
    ax1.set_xlabel('Time [ms]')
    
    ax2 = fig.add_subplot(212)
    ax2.set_xlim(0, eye_data_total['time'].max())
    ax2.plot(eye_data_total[(eye_data_total['stimuli'] == 'uas')]['time'],eye_data_total[(eye_data_total['stimuli'] == 'uas')][plot_axis], color='g')
    ax2.plot(eye_data_total[(eye_data_total['stimuli'] == 'aus')]['time'],eye_data_total[(eye_data_total['stimuli'] == 'aus')][plot_axis], color='m')
    legend(('Attractive on Stimulus Side','Unattractive on Stimulus Side'), bbox_to_anchor=(0.93, 1), shadow=False, frameon=False, prop=FontProperties(size=str(9*fontscale)))
    ax2.axhline(0, color='k', alpha = 0.1, linewidth=linewidth)
    ax2.axvline(sa_reaction_time, color='g', alpha = 0.3, linewidth=linewidth)
    ax2.axvline(su_reaction_time, color='m', alpha = 0.3, linewidth=linewidth)
    ax2.set_ylabel('X-axis % (towards stimulus)')
    ax2.set_xlabel('Time [ms]')

if __name__ == '__main__':
    ett()
    show()
