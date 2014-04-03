from __future__ import division
__author__ = 'Horea Christian'
import numpy as np

def means_from_id(lelist):
    lelist = lelist[lelist[:,0].argsort()] #sort by file name
    uniques = list(set(lelist[:,0])) # get unique names
    b = np.empty((len(uniques), len(lelist[0])), dtype = 'S24')   # create destination array for means
    for i,s in enumerate(uniques):
        m = lelist[:,0] == s
        b[i] = [s] + [lelist[m,j].astype(float).mean() for j in [1,2]] + [int(lelist[m,3].astype(float).mean())]
    return b

def open_csv(filename):
	import csv
	contents = []
	lefile = open(filename + '.csv', 'r')
	readfile = csv.reader(lefile, delimiter =',')
	for row in readfile:
		contents.append(row)
	lefile.close()
	return contents

def save_csv(filename, firstline=[]):
    from os import path, makedirs
    from shutil import move
    from datetime import date, datetime
    import csv
    filename
    jzt=datetime.now()
    time = str(date.today())+'_'+str(jzt.hour)+str(jzt.minute)+str(jzt.second)
    if path.isfile(filename):
        if path.isdir(path.dirname(filename)+'/.backup'):
            pass
        else: makedirs(path.dirname(filename)+'/.backup')        
        newname = path.dirname(filename)+'/.backup/'+path.splitext(path.basename(filename))[0]+'_'+time+path.splitext(path.basename(filename))[1]
        move(filename, newname)
        print 'moved pre-existing data file '+ filename +' to backup location ('+newname+')'
    else: pass
    datafile = open(filename, 'a')
    datawriter = csv.writer(datafile, delimiter=',')
    #print first line
    datawriter.writerow(firstline)
    return datawriter, datafile
    
def get_dataframes(id_list, bhpath):
	import pandas as pd
	conts = pd.DataFrame([])
	for i in id_list:
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
		cont['subblock'] = ''
		cont.ix[(cont['isstimleft'] == False) & (cont['block'] == 'au'), 'subblock'] = 'aus+sua'
		cont.ix[(cont['isstimleft'] == False) & (cont['block'] == 'ua'), 'subblock'] = 'uas+sau'
		cont.ix[(cont['isstimleft'] == True) & (cont['block'] == 'au'), 'subblock'] = 'uas+sau'
		cont.ix[(cont['isstimleft'] == True) & (cont['block'] == 'ua'), 'subblock'] = 'aus+sua'
		#meanscont = cont.groupby('subblock').mean()
		#print meanscont
		#cat1 = cont[cont['subblock']=='aus+sua']
		#cat2 = cont[cont['subblock']=='uas+sau']
		#print ttest_ind(cat1['RT'], cat2['RT'])
		cont['RTdiff'] = ''
		cont['RTdiff'] = cont['RT']-cont[(cont['block'] == 'uu') | (cont['block'] == 'aa')]['RT'].mean()
		conts = pd.concat([conts, cont], ignore_index=True)
	return conts
	
def get_dataframes_for_dp(id_list, bhpath):
	import pandas as pd
	from scipy.stats import norm
	import numpy as np
	t_cr_au =0
	t_fa_au =0
	t_ht_au =0
	t_ms_au =0
	all_au_dp = np.zeros((len(id_list),1), dtype = np.float) # all the attractive-unattractive dp values 
	
	t_cr_aa =0
	t_fa_aa =0
	t_ht_aa =0
	t_ms_aa =0
	all_aa_dp = np.zeros((len(id_list),1), dtype = np.float) # all the attractive-unattractive dp values
	
	t_cr_uu =0
	t_fa_uu =0
	t_ht_uu =0
	t_ms_uu =0
	all_uu_dp = np.zeros((len(id_list),1), dtype = np.float) # all the attractive-unattractive dp values
	for ix, i in enumerate(id_list):
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
		
		
		#FAR:
		cr_a_au = cont[(cont['rateL'] >= score_top) & (cont['rateR'] <= score_top) & (cont['isstimleft'] == False) & (cont['keypress'] == 'right')].count().ix[0] 
		cr_b_au = cont[(cont['rateL'] <= score_top) & (cont['rateR'] >= score_top) & (cont['isstimleft'] == True) & (cont['keypress'] == 'left')].count().ix[0]
		cr_au = (cr_a_au+cr_b_au)/2 # correct rejections (d-prime)
		fa_a_au = cont[(cont['rateL'] >= score_top) & (cont['rateR'] <= score_top) & (cont['isstimleft'] == False) & (cont['keypress'] == 'left')].count().ix[0]
		fa_b_au = cont[(cont['rateL'] <= score_top) & (cont['rateR'] >= score_top) & (cont['isstimleft'] == True) & (cont['keypress'] == 'right')].count().ix[0]
		fa_au = (fa_a_au + fa_b_au)/2 # false alarm (d-prime)
		
		far_au= fa_au / (fa_au+cr_au) # false alarm rate
		if far_au == 1: # make sure far is not 0 or 1 (gives +/-inf for z score)
			far_au = (fa_au+cr_au-0.01)/(fa_au+cr_au)
		if far_au == 0:
			far_au = 0.01/(fa_au+cr_au)
		
		#HR:
		ht_a_au = cont[(cont['rateL'] >= score_top) & (cont['rateR'] <= score_top) & (cont['isstimleft'] == True) & (cont['keypress'] == 'left')].count().ix[0] 
		ht_b_au = cont[(cont['rateL'] <= score_top) & (cont['rateR'] >= score_top) & (cont['isstimleft'] == False) & (cont['keypress'] == 'right')].count().ix[0]
		ht_au = (ht_a_au+ht_b_au)/2 # correct hits (d-prime)
		ms_a_au = cont[(cont['rateL'] >= score_top) & (cont['rateR'] <= score_top) & (cont['isstimleft'] == True) & (cont['keypress'] == 'right')].count().ix[0]
		ms_b_au = cont[(cont['rateL'] <= score_top) & (cont['rateR'] >= score_top) & (cont['isstimleft'] == False) & (cont['keypress'] == 'left')].count().ix[0]
		ms_au = (ms_a_au + ms_b_au)/2 # miss (d-prime)
	
		
		hr_au = ht_au / (ht_au+ms_au) # hit rate
		if hr_au == 1: # make sure hr is not 0 or 1 (gives +/-inf for z score) 
			hr_au = (ht_au+ms_au-0.01)/(ht_au+ms_au)
		if hr_au == 0:
			hr_au = 0.01/(ht_au+ms_au)
		
		zhr_au = norm.ppf(hr_au)
		zfar_au = norm.ppf(far_au)
		dp_au = zhr_au-zfar_au
		
		#population values:
		all_au_dp[ix] =  dp_au
		t_cr_au = t_cr_au + cr_au
		t_fa_au= t_fa_au + fa_au
		t_ht_au= t_ht_au + ht_au
		t_ms_au= t_ms_au + ms_au
		
		#FAR:
		cr_aa = cont[(cont['rateL'] >= score_top) & (cont['rateR'] >= score_top) & (cont['isstimleft'] == False) & (cont['keypress'] == 'right')].count().ix[0] 
		fa_aa = cont[(cont['rateL'] >= score_top) & (cont['rateR'] >= score_top) & (cont['isstimleft'] == False) & (cont['keypress'] == 'left')].count().ix[0]
		
		far_aa= fa_aa / (fa_aa+cr_aa) # false alarm rate
		if far_aa == 1: # make sure far is not 0 or 1 (gives +/-inf for z score)
			far_aa = (fa_aa+cr_aa-0.01)/(fa_aa+cr_aa)
		if far_aa == 0:
			far_aa = 0.01/(fa_aa+cr_aa)
		
		#HR:
		ht_aa = cont[(cont['rateL'] >= score_top) & (cont['rateR'] >= score_top) & (cont['isstimleft'] == True) & (cont['keypress'] == 'left')].count().ix[0] 
		ms_aa = cont[(cont['rateL'] >= score_top) & (cont['rateR'] >= score_top) & (cont['isstimleft'] == True) & (cont['keypress'] == 'right')].count().ix[0]
	
		
		hr_aa= ht_aa / (ht_aa+ms_aa) # false alarm rate
		if hr_aa == 1: # make sure far is not 0 or 1 (gives +/-inf for z score)
			hr_aa = (ht_aa+ms_aa-0.01)/(ht_aa+ms_aa)
		if hr_aa == 0:
			hr_aa = 0.01/(ht_aa+ms_aa)
		
		zhr_aa = norm.ppf(hr_aa)
		zfar_aa = norm.ppf(far_aa)
		dp_aa = zhr_aa-zfar_aa
		
		#population values:
		all_aa_dp[ix] =  dp_aa
		t_cr_aa = t_cr_aa + cr_aa
		t_fa_aa= t_fa_aa + fa_aa
		t_ht_aa= t_ht_aa + ht_aa
		t_ms_aa= t_ms_aa + ms_aa
		
		#FAR:
		cr_uu = cont[(cont['rateL'] <= score_top) & (cont['rateR'] <= score_top) & (cont['isstimleft'] == False) & (cont['keypress'] == 'right')].count().ix[0] 
		fa_uu = cont[(cont['rateL'] <= score_top) & (cont['rateR'] <= score_top) & (cont['isstimleft'] == False) & (cont['keypress'] == 'left')].count().ix[0]
		
		far_uu= fa_uu / (fa_uu+cr_uu) # false alarm rate
		if far_uu == 1: # make sure far is not 0 or 1 (gives +/-inf for z score)
			far_uu = (fa_uu+cr_uu-0.01)/(fa_uu+cr_uu)
		if far_uu == 0:
			far_uu = 0.01/(fa_uu+cr_uu)
		
		#HR:
		ht_uu = cont[(cont['rateL'] <= score_top) & (cont['rateR'] <= score_top) & (cont['isstimleft'] == True) & (cont['keypress'] == 'left')].count().ix[0] 
		ms_uu = cont[(cont['rateL'] <= score_top) & (cont['rateR'] <= score_top) & (cont['isstimleft'] == True) & (cont['keypress'] == 'right')].count().ix[0]
		
		hr_uu= ht_uu / (ht_uu+ms_uu) # false alarm rate
		if hr_uu == 1: # make sure far is not 0 or 1 (gives +/-inf for z score)
			hr_uu = (ht_uu+ms_uu-0.01)/(ht_uu+ms_uu)
		if hr_uu == 0:
			hr_uu = 0.01/(ht_uu+ms_uu)
		
		zhr_uu = norm.ppf(hr_uu)
		zfar_uu = norm.ppf(far_uu)
		dp_uu = zhr_uu-zfar_uu
		
		#population values:
		all_uu_dp[ix] =  dp_uu
		t_cr_uu = t_cr_uu + cr_uu
		t_fa_uu= t_fa_uu + fa_uu
		t_ht_uu= t_ht_uu + ht_uu
		t_ms_uu= t_ms_uu + ms_uu

	print t_cr_au,t_fa_au,t_ht_au,t_ms_au,t_cr_aa,t_fa_aa,t_ht_aa,t_ms_aa,t_cr_uu,t_fa_uu,t_ht_uu,t_ms_uu
	return t_cr_au,t_fa_au,t_ht_au,t_ms_au,t_cr_aa,t_fa_aa,t_ht_aa,t_ms_aa,t_cr_uu,t_fa_uu,t_ht_uu,t_ms_uu, all_au_dp, all_aa_dp, all_uu_dp


def get_scatterdata(id_list,bhpath):
	import pandas as pd
	#from scipy.stats import pearsonr
	conts = pd.DataFrame([])
	for i in id_list:
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
		
		#cont = cont[(cont['block']=='au')|(cont['block']=='ua')]
		
		cont1 = cont[cont['isstimleft'] == False]
		cont1['ratediff'] = cont1['rateR'] - cont['rateL']
		cont2 = cont[cont['isstimleft'] == True]
		cont2['ratediff'] = cont2['rateL'] - cont['rateR']
		cont = pd.concat([cont1,cont2])
		#print pearsonr(cont['ratediff'], cont['RT'])
		cont['RTdiff'] = ''
		cont['RTdiff'] = cont['RT']-cont['RT'].mean()
		conts = pd.concat([conts, cont])
	return conts
	
