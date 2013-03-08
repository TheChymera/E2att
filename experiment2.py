#!/usr/bin/env python
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
__author__ = 'Horea Christian'
from psychopy import core, visual, gui, data, event
from math import ceil
from numpy.random import permutation
from os import listdir
from letobii import TobiiController
import time
import csv
import numpy as np
import sys

################################
### Experiment variables 
################################
wm_trial_repeat=6 #even number, to maintain 1:1 left/rigt cue pressentation ratio
wm_trial_cond=8
pic_group_N=10 #how many pictures in each group (attractive//unattractive)

#TIMES (in [ms]):
fixationtime = 2 # s instead of ms
att_time = 2 # s instead of ms
rate_time = 3
pause = 2

#MONITOR SPECS:
resolution = [1920, 1080]
################################
### END Experiment variables 
################################

pic_repeat = ceil(wm_trial_repeat * wm_trial_cond / pic_group_N) # calculate necessary repeats

expInfo = {'Identifier':'','Most attracted to':['female faces','male faces']}

dlg = gui.DlgFromDict(expInfo, title='Experiment1', fixed=['date'])
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr(format="%m-%d_%H-%M")  # add a simple timestamp

#General variables:
if expInfo['Most attracted to'] == 'male faces':
    face_gender = 'm'
    img_path='pics/male/'
else:
    img_path='pics/female/'
    face_gender = 'f'
    
fileName = 'results/' +  expInfo['Identifier'] + '_' + face_gender + '_' + 'p' + expInfo['date']
fileName2 = 'results/' + expInfo['Identifier'] + '_' + face_gender + '_' +'wm' + expInfo['date']
eyedata = 'results/testdata.tsv'
dataFile = open(fileName+'.csv', 'a')
dataWriter = csv.writer(dataFile, delimiter=',')
dataWriter.writerow(['nameL','rateL','nameR','rateR', 'isstimleft', 'keypress', 'RT', 'session'])
dataFile2 = open(fileName2+'.csv', 'a')
dataWriter2 = csv.writer(dataFile2, delimiter=',')
dataWriter2.writerow(['picture','score','RT','session'])
pictures = listdir(img_path)
pictures = [{'name': x.decode('ascii')} for x in pictures]

#windows:
win = visual.Window(resolution, color=[1,1,1],fullscr=True,allowGUI=False,monitor="testMonitor", screen=1, units="deg")
win.setRecordFrameIntervals(True)

#experiments:
fpref_epx = data.ExperimentHandler(name='Face Preference', version='0.0.1', extraInfo=expInfo, saveWideText=False, dataFileName=fileName)
attwm_exp = data.ExperimentHandler(name='att-wm', version='0.0.1', extraInfo=expInfo, saveWideText=False, dataFileName=fileName)

#loops:
face_loop = data.TrialHandler(pictures, 1)
fpref_epx.addLoop(face_loop)  # add the loop to the experiment
face_loop_val = face_loop.trialList[0]  # so we can initialise stimuli with some values

#stimuli:
circle = visual.Circle(win, radius=0.2, edges=133, lineColor=(0 , 0, 0), fillColor=(0 , 0, 0))# radii chosen so that the area of the square and circle are identical
square = visual.Circle(win, radius=0.25, edges=4, lineColor=(0 , 0, 0), fillColor=(0 , 0, 0)) #idem
fixation = visual.Circle(win, radius=0.1, edges=133, lineColor=(0 , 0, 0), fillColor=(0 , 0, 0))
message1 = visual.TextStim(win, pos=[0,2],color=[0,0,0],text='Rate the following faces according to how attracted you feel towards them.\
    \n\nIn between presentations concentrate on the fixation dot (in the middle of the screen).\n\nPress any key to continue',wrapWidth=20.0)
message2 = visual.TextStim(win, pos=[0,2],color=[0,0,0],text='Please wait...',wrapWidth=20.0)
message3 = visual.TextStim(win, pos=[0,2],color=[0,0,0],text='Select in each screen the position (left/right, as relative to yourself) where\
    the circle is located. \n\nIndicate your choice by pressing the left or right arrow keys on the keyboard as rapidly as possible.\
    \n\nPress any key to continue',wrapWidth=20.0)
message4 = visual.TextStim(win, pos=[0,2],color=[0,0,0],text='Thank you very much for completing the test.\n\nPlease report to your experimenter.'
                           ,wrapWidth=20.0)
image = visual.ImageStim(win, name='image',image='sin', mask=None,ori=0, pos=[0, 0], size=[9.9,13.2],color=[1,1,1], colorSpace=u'rgb',
    opacity=1,texRes=128, interpolate=True, depth=0.0)
image_l = visual.ImageStim(win, name='image',image='sin', mask=None,ori=0, pos=[6,0], size=[9,12],color=[1,1,1], colorSpace=u'rgb',
    opacity=1,texRes=128, interpolate=True, depth=0.0)
image_r = visual.ImageStim(win, name='image',image='sin', mask=None,ori=0, pos=[-6,0], size=[9,12],color=[1,1,1], colorSpace=u'rgb',
    opacity=1,texRes=128, interpolate=True, depth=0.0)
rating = visual.RatingScale(win=win, name='rating', displaySizeFactor=1.00, escapeKeys=['escape'],textSizeFactor=0.8, lineColor='DarkGrey',
    pos=[0.0, -0.1], low=0, high=1, showScale=False, lowAnchorText='not at all attracted', highAnchorText='very attracted',stretchHoriz=1.2,
    precision=100, showValue=False, markerExpansion=0, singleClick=False,markerStyle='glow', markerColor='#444444')
#and some handy clocks to keep track of time
globalClock = core.Clock()
trialClock = core.Clock()
#Eye tracking (Tobii)
controller = TobiiController(win)
controller.setDataFile(eyedata)
controller.waitForFindEyeTracker()
controller.activate(controller.eyetrackers.keys()[0])
while True:
    ret = controller.doCalibration([(0.1,0.1), (0.9,0.1) , (0.5,0.5), (0.1,0.9), (0.9,0.9)])
    if ret == 'accept':
        break
    elif ret == 'abort':
        controller.destroy()
        sys.exit()
marker = visual.Rect(win,width=5,height=5)
controller.startTracking()


#START DISPLAYING
message1.draw()
win.flip()#to show our newly drawn 'stimuli'
event.waitKeys()#pause until there's a keypress
#RATING TRIALS
for ix, face_loop_val in enumerate(face_loop):
    image.setImage(img_path + face_loop_val['name'])
    rating.reset()
    t = 0
    #Fixation
    fixation.draw(win)
    win.flip()
    core.wait(fixationtime,fixationtime)
    #Picture
    win.setRecordFrameIntervals(False)
    image.draw()
    win.flip()
    win.setRecordFrameIntervals(True)
    trialClock.reset() #Put this after the fixation win.flip if you want to count fixation as part of the trial.
    core.wait(rate_time,rate_time)
    continueRoutine = True
    while continueRoutine:
        rating.draw()
        win.setMouseVisible(True)
        win.flip()
        continueRoutine = rating.noResponse
    win.setMouseVisible(False)
    dataWriter.writerow([face_loop_val['name'], str(rating.getRating()), str(rating.getRT()), ix])
dataFile.close()
win.flip()
message2.draw()
win.flip()
time.sleep(3)
# stimulus file for wm-att trial
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
#instructions wm-att trial
message3.draw()
win.flip()
event.waitKeys()#pause until there's a keypress
# stimuli = stimuli[:2] # curtail stimuli for test purposes
# new loops
tb_pictures = [{'namel': x[0], 'ratel': x[1], 'namer': x[3], 'rater': x[4], 'stiml': x[6]} for x in stimuli]
attwm_loop = data.TrialHandler(tb_pictures, 1)
# ATTENTION TRIALS
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
    win.setRecordFrameIntervals(False)
    image_l.draw(win)
    image_r.draw(win)
    circle.draw(win)
    square.draw(win)
    win.flip()
    win.setRecordFrameIntervals(True)
    trialClock.reset() #Put this after the fixation win.flip if you want to count fixation as part of the trial.
    core.wait(att_time,att_time)
    keypress = event.getKeys(keyList=None,timeStamped=trialClock)
    keypress = np.array(keypress)
    if keypress == []:
        continue
    dataWriter2.writerow([attwm_loop_val['namel'], attwm_loop_val['ratel'], attwm_loop_val['namer'], attwm_loop_val['rater'], attwm_loop_val['stiml'], 
                          keypress[0][0], keypress[0][1], ix])
message4.draw()
win.flip()
time.sleep(5)
win.close()