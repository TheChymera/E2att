#!/usr/bin/env python
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
__author__ = 'Horea Christian'
from psychopy import core, visual, gui, monitors
from os import listdir
from experiments import eyetracker, rate_experiment, st_experiment
import time

#EXPERIMENT VARIABLES
#Subexperiments:
eyetracker_do = True
rate_experiment_do = True
st_experiment_do = True

#Times (in [s]):
fixationtime = 2
end_pause = 5

#Monitor specs:
mymon = monitors.Monitor('testMonitor', width=51, distance=53)
resolution = [1920, 1080]
#END EXPERIMENT VARIABLES

#INTERACTING W/ PARTICIPANT
expInfo = {'Identifier':'','Most attracted to':['female faces','male faces']}
dlg = gui.DlgFromDict(expInfo, title='Experiment1')
if dlg.OK == False: core.quit()  # user pressed cancel
#END INTERACTING W/ PARTICIPANT

#windows:
win = visual.Window(resolution, color=[1,1,1],fullscr=True,allowGUI=False,monitor=mymon, screen=1, units="deg")
win.setRecordFrameIntervals(False)

#stimuli:
fixation = visual.Circle(win, radius=0.15, edges=64, lineColor=(0 , 0, 0), fillColor=(0 , 0, 0), interpolate=True)
message2 = visual.TextStim(win, pos=[0,2],color=[0,0,0],text='Please wait...',wrapWidth=20.0)
fin_message = visual.TextStim(win, pos=[0,2],color=[0,0,0],text='Thank you very much for completing the test.\n\nPlease report to your experimenter.'
                           ,wrapWidth=20.0)
 
#clocks:
globalClock = core.Clock()
trialClock = core.Clock()


if expInfo['Most attracted to'] == 'male faces':
    face_gender = 'm'
    img_path='pics/male/'
else:
    img_path='pics/female/'
    face_gender = 'f'
pictures = listdir(img_path)
pictures = [{'name': x.decode('ascii')} for x in pictures]

#EXPERIMENT FILES

if rate_experiment_do:
    if eyetracker_do:
        controller = eyetracker(win, expInfo, face_gender, 'p')
    ratingfilename = rate_experiment(win, expInfo, face_gender, img_path, pictures, fixation, fixationtime, trialClock, controller, eyetracker_do)
else: ratingfilename = None
if st_experiment_do:
    if eyetracker_do: 
        controller = eyetracker(win, expInfo, face_gender, 'wm')
    else: controller = None
    message2.draw()
    win.flip()
    st_experiment(win, expInfo, face_gender, img_path, fixation, fixationtime, trialClock, ratingfilename, controller, eyetracker_do)

fin_message.draw()
win.flip()
time.sleep(end_pause)
win.close()
