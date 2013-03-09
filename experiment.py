#!/usr/bin/env python
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
__author__ = 'Horea Christian'
from psychopy import core, visual, gui, data
from letobii import TobiiController
from os import listdir
#from lebrowser import EyetrackerBrowser
import time
import sys

#EXPERIMENT VARIABLES
#Times (in [s]):
fixationtime = 2
end_pause = 5

#Monitor specs:
resolution = [1920, 1080]
#END EXPERIMENT VARIABLES

#Files:
eyedata = 'results/testdata.tsv'

#windows:
win = visual.Window(resolution, color=[1,1,1],fullscr=True,allowGUI=False,monitor="testMonitor", screen=1, units="deg")
win.setRecordFrameIntervals(False)

#stimuli:
fixation = visual.Circle(win, radius=0.1, edges=133, lineColor=(0 , 0, 0), fillColor=(0 , 0, 0))
fin_message = visual.TextStim(win, pos=[0,2],color=[0,0,0],text='Thank you very much for completing the test.\n\nPlease report to your experimenter.'
                           ,wrapWidth=20.0)
						   
#and some handy clocks to keep track of time
globalClock = core.Clock()
trialClock = core.Clock()

#INTERACTING W/ PARTICIPANT
expInfo = {'Identifier':'','Most attracted to':['female faces','male faces']}
dlg = gui.DlgFromDict(expInfo, title='Experiment1', fixed=['date'])
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr(format="%m-%d_%H-%M")  # add a simple timestamp
#END INTERACTING W/ PARTICIPANT

if expInfo['Most attracted to'] == 'male faces':
    face_gender = 'm'
    img_path='pics/male/'
else:
    img_path='pics/female/'
    face_gender = 'f'
pictures = listdir(img_path)
pictures = [{'name': x.decode('ascii')} for x in pictures]
#Files:
eyedata = 'results/' +  expInfo['Identifier'] + '_' + face_gender + '_' + 'et' + expInfo['date'] + '.tsv'

#Eye tracking (Tobii)
controller = TobiiController(win)
controller.setDataFile(eyedata)
controller.waitForFindEyeTracker()
controller.activate(controller.eyetrackers.keys()[0])
#INTERACTING W/ PARTICIPANT
while True:
    ret = controller.doCalibration([(0.1,0.1), (0.9,0.1) , (0.5,0.5), (0.1,0.9), (0.9,0.9)])
    if ret == 'accept':
        break
    elif ret == 'abort':
        controller.destroy()
        sys.exit()
marker = visual.Rect(win,width=5,height=5)
#END INTERACTING W/ PARTICIPANT

#EXPERIMENT FILES

#execfile('experiment1.py')
#message2.draw()
#win.flip()
execfile('experiment2.py')

fin_message.draw()
win.flip()
time.sleep(end_pause)
win.close()