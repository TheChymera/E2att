__author__ = 'Horea Christian'
from psychopy import event
import csv

#EXPERIMENT VARIABLES
#Times (in [s]):
rate_time = 3
#END EXPERIMENT VARIABLES
    
fileName = 'results/' +  expInfo['Identifier'] + '_' + face_gender + '_' + 'p' + expInfo['date']
eyedata = 'results/testdata.tsv'
dataFile = open(fileName+'.csv', 'a')
dataWriter = csv.writer(dataFile, delimiter=',')
dataWriter.writerow(['picture','score','RT','session'])

#experiments:
fpref_epx = data.ExperimentHandler(name='Face Preference', version='0.0.1', extraInfo=expInfo, saveWideText=False, dataFileName=fileName)

#loops:
face_loop = data.TrialHandler(pictures, 1)
fpref_epx.addLoop(face_loop)  # add the loop to the experiment
face_loop_val = face_loop.trialList[0]  # so we can initialise stimuli with some values

#stimuli:
message1 = visual.TextStim(win, pos=[0,2],color=[0,0,0],text='Rate the following faces according to how attracted you feel towards them.\
    \n\nIn between presentations concentrate on the fixation dot (in the middle of the screen).\n\nPress any key to continue',wrapWidth=20.0)
message2 = visual.TextStim(win, pos=[0,2],color=[0,0,0],text='Please wait...',wrapWidth=20.0)
image = visual.ImageStim(win, name='image',image='sin', mask=None,ori=0, pos=[0, 0], size=[9.9,13.2],color=[1,1,1], colorSpace=u'rgb',
    opacity=1,texRes=128, interpolate=True, depth=0.0)
rating = visual.RatingScale(win=win, name='rating', displaySizeFactor=1.00, escapeKeys=['escape'],textSizeFactor=0.8, lineColor='DarkGrey',
    pos=[0.0, -0.1], low=0, high=1, showScale=False, lowAnchorText='not at all attracted', highAnchorText='very attracted',stretchHoriz=1.2,
    precision=100, showValue=False, markerExpansion=0, singleClick=False,markerStyle='glow', markerColor='#444444')

#INTERACTING W/ PARTICIPANT
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
    image.draw()
    win.flip()
    win.setRecordFrameIntervals(True)
    controller.startTracking()
    trialClock.reset() #Put this after the fixation win.flip if you want to count fixation as part of the trial.
    core.wait(rate_time,rate_time)
    continueRoutine = True
    controller.stopTracking()
    while continueRoutine:
        rating.draw()
        win.setMouseVisible(True)
        win.flip()
        continueRoutine = rating.noResponse
    win.setMouseVisible(False)
    win.setRecordFrameIntervals(False)
#    controller.lereset()
    dataWriter.writerow([face_loop_val['name'], str(rating.getRating()), str(rating.getRT()), ix])
dataFile.close()
#END INTERACTING W/ PARTICIPANT