from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
__author__ = 'Horea Christian'
from psychopy import core, visual, gui, data, event
from math import ceil
from numpy.random import permutation
from os import listdir
from letobii import TobiiController
#from lebrowser import EyetrackerBrowser
import time
import csv
import numpy as np
import sys


#EXPERIMENT VARIABLES
#Session repeats et al.
wm_trial_repeat=6 #even number, to maintain 1:1 left/rigt cue pressentation ratio
wm_trial_cond=8
pic_group_N=5 #how many pictures in each group (attractive//unattractive)

#Times (in [s]):
att_time = 2
process_paddingtime = 3

#Preset input
preset_attfile = 'd#_f_wm03-09_06-05'
#END EXPERIMENT VARIABLES

#File names	
if preset_attfile:
    fileName = 'results/' + preset_attfile
else:
    fileName = 'results/' +  expInfo['Identifier'] + '_' + face_gender + '_' + 'p' + expInfo['date']

fileName2 = 'results/' + expInfo['Identifier'] + '_' + face_gender + '_' +'wm' + expInfo['date']
dataFile2 = open(fileName2+'.csv', 'a')
dataWriter2 = csv.writer(dataFile2, delimiter=',')
dataWriter2.writerow(['nameL','rateL','nameR','rateR', 'isstimleft', 'keypress', 'RT', 'session'])

#CREATE STIMULUS INDEX
pic_repeat = ceil(wm_trial_repeat * wm_trial_cond / pic_group_N) # calculate necessary repeats
pics=[]
dataFile = open(fileName+'.csv', 'r')
readfile = csv.reader(dataFile, delimiter =',')
for row in readfile:
    pics.append(row)
dataFile.close()
pics = np.array(pics[1:][:])
pics_sort = pics[pics[:,1].argsort()] #sorted by attractiveness, argsort gives a row number's list so that the column is ascending
top_pics = pics_sort[-pic_group_N:,:]
bottom_pics = pics_sort[:pic_group_N,:]
top_pics_stack = np.tile(top_pics, (pic_repeat, 1))
top_pics_stack = top_pics_stack[permutation(len(top_pics_stack))]
bottom_pics_stack = np.tile(bottom_pics, (pic_repeat, 1))
bottom_pics_stack = bottom_pics_stack[permutation(len(bottom_pics_stack))]
lcue = np.tile([['True'], ['False']], (wm_trial_repeat/2,1))
cond_1= np.concatenate((top_pics_stack[0:wm_trial_repeat], bottom_pics_stack[0:wm_trial_repeat], lcue), axis=1)
cond_2= np.concatenate((bottom_pics_stack[wm_trial_repeat:wm_trial_repeat*2], top_pics_stack[wm_trial_repeat:wm_trial_repeat*2], lcue), axis=1)
cond_3= np.concatenate((bottom_pics_stack[wm_trial_repeat*2:wm_trial_repeat*3], bottom_pics_stack[wm_trial_repeat*3:wm_trial_repeat*4], lcue), axis=1)
cond_4= np.concatenate((top_pics_stack[wm_trial_repeat*2:wm_trial_repeat*3], top_pics_stack[wm_trial_repeat*3:wm_trial_repeat*4], lcue), axis=1)
stimuli = np.concatenate((cond_1, cond_2, cond_3, cond_4), axis=0)
#END CREATE STIMULUS INDEX

#stimuli:
circle = visual.Circle(win, radius=0.2, edges=133, lineColor=(0 , 0, 0), fillColor=(0 , 0, 0))# radii chosen so that the area of the square and circle are identical
square = visual.Circle(win, radius=0.25, edges=4, lineColor=(0 , 0, 0), fillColor=(0 , 0, 0)) #idem
message3 = visual.TextStim(win, pos=[0,2],color=[0,0,0],text='Select in each screen the position (left/right, as relative to yourself) where\
    the circle is located. \n\nIndicate your choice by pressing the left or right arrow keys on the keyboard as rapidly as possible.\
    \n\nPress any key to continue',wrapWidth=20.0)
image_l = visual.ImageStim(win, name='image',image='sin', mask=None,ori=0, pos=[6,0], size=[9,12],color=[1,1,1], colorSpace=u'rgb',
    opacity=1,texRes=128, interpolate=True, depth=0.0)
image_r = visual.ImageStim(win, name='image',image='sin', mask=None,ori=0, pos=[-6,0], size=[9,12],color=[1,1,1], colorSpace=u'rgb',
    opacity=1,texRes=128, interpolate=True, depth=0.0)
time.sleep(process_paddingtime)

# new loops
tb_pictures = [{'namel':x[0],'ratel':x[1],'RTl':x[2],'orderl':x[3],'namer':x[4],'rater':x[5],
'RTr':x[6],'orderr':x[7],'stiml': x[8]} for x in stimuli]
attwm_loop = data.TrialHandler(tb_pictures, 1)

#INTERACTING W/ PARTICIPANT
message3.draw()
win.flip()
event.waitKeys()#pause until there's a keypress

for ix, attwm_loop_val in enumerate(attwm_loop):
    image_l.setImage(img_path + attwm_loop_val['namel'])
    image_r.setImage(img_path + attwm_loop_val['namer'])
    if attwm_loop_val['stiml'] == 'False':
        circle.setPos((11,0))
        square.setPos((-11,0))
    else:
        circle.setPos((-11,0))
        square.setPos((11,0))
    t = 0 
    #Fixation
    fixation.draw(win)
    win.flip()
    core.wait(fixationtime,fixationtime)
    #Targets
    image_l.draw(win)
    image_r.draw(win)
    circle.draw(win)
    square.draw(win)
    win.flip()
    win.setRecordFrameIntervals(True)
    controller.startTracking()
    trialClock.reset() #Put this after the fixation win.flip if you want to count fixation as part of the trial.
    core.wait(att_time,att_time)
    keypress = event.getKeys(keyList=None,timeStamped=trialClock)
    keypress = np.array(keypress)
    if keypress == []:
        print 'aaa'
        keypress = np.array(['none',2])
    elif keypress != []:
	    print 'bbb'
    print keypress
    win.setRecordFrameIntervals(False)
    controller.stopTracking()
    dataWriter2.writerow([attwm_loop_val['namel'],attwm_loop_val['ratel'],attwm_loop_val['RTl'],
	attwm_loop_val['orderl'],attwm_loop_val['namer'],attwm_loop_val['rater'],attwm_loop_val['RTr'],
	attwm_loop_val['orderr'],attwm_loop_val['stiml'],keypress[0][0], keypress[0][1], ix])
#END INTERACTING W/ PARTICIPANT