__author__ = 'Horea Christian'
from psychopy import visual, data, event, core
from lefunctions import save_csv
import csv

def rate_experiment(win, expInfo, face_gender, img_path, pictures, fixation, fixationtime, trialClock, controller=None, eyetracker_do=False):
    from random import choice

    #EXPERIMENT VARIABLES
    #Times (in [s]):
    rate_time = 2
    #END EXPERIMENT VARIABLES

    ratingfilename = 'results/' +  expInfo['Identifier'] + '_' + face_gender + '_' + 'p' + '.csv'
    ratingwriter, ratingfile = save_csv(ratingfilename, ['picture','score','RT','session'])

    #loops:
    face_loop = data.TrialHandler(pictures, 3)
    face_loop_val = face_loop.trialList[0]  # so we can initialise stimuli with some values

    #stimuli:
    message1 = visual.TextStim(win, pos=[0,2],color=[0,0,0],text='Rate the following faces according to how attracted you feel towards them.\
        \n\nIn between presentations concentrate on the fixation dot (in the middle of the screen).\n\nPress any key to continue',wrapWidth=20.0)
    image = visual.ImageStim(win, name='image',image='sin', mask=None,ori=0, pos=[0, 0], size=[19.5,26],color=[1,1,1], colorSpace=u'rgb',
        opacity=1,texRes=128, interpolate=True, depth=0.0)
    rating = visual.RatingScale(win=win, name='rating', displaySizeFactor=1.00, escapeKeys=['escape'],textSizeFactor=0.8, lineColor='DarkGrey',
        pos=[0.0, -0.1], low=0, high=1, showScale=False, lowAnchorText='not at all attracted', highAnchorText='very attracted',stretchHoriz=1.2,
        precision=100, showValue=False, markerExpansion=0, singleClick=False,markerStyle='glow', markerColor='#444444')

    #INTERACTING W/ PARTICIPANT
    message1.draw()
    win.flip()#to show our newly drawn 'stimuli'
    event.waitKeys()#pause until there's a keypress

    image.setImage(img_path + choice(face_loop.trialList)['name'])
    #Fixation
    fixation.draw(win)
    win.flip()
    core.wait(fixationtime,fixationtime)
    #Picture
    image.draw()
    win.flip()
    if controller:
        controller.startTracking()
    trialClock.reset() #Put this after the fixation win.flip if you want to count fixation as part of the trial.
    core.wait(rate_time,rate_time)
    continueRoutine = True
    if controller:
        controller.stopTracking()
    while continueRoutine:
        rating.draw()
        win.setMouseVisible(True)
        win.flip()
        continueRoutine = rating.noResponse
    win.setMouseVisible(False)

    #RATING TRIALS
    for ix, face_loop_val in enumerate(face_loop):
        image.setImage(img_path + face_loop_val['name'])
        rating.reset()
        #Fixation
        fixation.draw(win)
        win.flip()
        core.wait(fixationtime,fixationtime)
        #Picture
        image.draw()
        win.flip()
        if controller:
            controller.startTracking()
        trialClock.reset() #Put this after the fixation win.flip if you want to count fixation as part of the trial.
        core.wait(rate_time,rate_time)
        continueRoutine = True
        if controller:
            controller.stopTracking()
        while continueRoutine:
            rating.draw()
            win.setMouseVisible(True)
            win.flip()
            continueRoutine = rating.noResponse
        win.setMouseVisible(False)
        ratingwriter.writerow([face_loop_val['name'], str(rating.getRating()), str(rating.getRT()), ix])
    ratingfile.close()
    #END INTERACTING W/ PARTICIPANT
    if eyetracker_do:
        from letobii import TobiiController
        controller.closeDataFile()
    return ratingfilename

def st_experiment(win, expInfo, face_gender, img_path, fixation, fixationtime, trialClock, ratingfilename=None, controller=None, eyetracker_do=False):
    from math import ceil
    from numpy.random import permutation
    from lefunctions import means_from_id
    import numpy as np


    #EXPERIMENT VARIABLES
    #Session repeats et al.
    wm_trial_repeat=30 #even number, to maintain 1:1 left/rigt cue pressentation ratio
    wm_trial_cond=4 # number of conditions - see how many cond_* variables you have below
    pic_group_N=20 #how many pictures in each group (attractive//unattractive)

    #Times (in [s]):
    att_time = 1.5
    process_paddingtime = 3

    #Preset input
    preset_attfile = 'aa7922847_m_p'
    #END EXPERIMENT VARIABLES

    wmfilename = 'results/' + expInfo['Identifier'] + '_' + face_gender + '_' +'wm' + '.csv'
    wmwriter,wmfile = save_csv(wmfilename, ['nameL','rateL','RTL','orderL','nameR','rateR','RTR','orderR','isstimleft','keypress','RT','session'])

    #CREATE STIMULUS INDEX
    pic_repeat = ceil(wm_trial_repeat * wm_trial_cond / pic_group_N) # calculate necessary repeats
    pics=[]
    if not ratingfilename:
        ratingfilename = 'results/' + expInfo['Identifier'] + '_' + face_gender +  '_p.csv'
    ratingfile = open(ratingfilename, 'r')
    readrating = csv.reader(ratingfile, delimiter =',')
    print(readrating)
    for row in readrating:
        pics.append(row)
    ratingfile.close()
    pics = np.array(pics[1:][:])
    pics = means_from_id(pics)
    pics_sort = pics[pics[:,1].argsort()] #sorted by attractiveness, argsort gives a row number's list so that the column is ascending
    top_pics = pics_sort[-pic_group_N:,:]
    bottom_pics = pics_sort[:pic_group_N,:]
    top_pics_stack = np.tile(top_pics, (pic_repeat, 1))
    top_pics_stack = top_pics_stack[permutation(len(top_pics_stack))]
    bottom_pics_stack = np.tile(bottom_pics, (pic_repeat, 1))
    bottom_pics_stack = bottom_pics_stack[permutation(len(bottom_pics_stack))]
    lcue = np.tile([['True'], ['False']], (wm_trial_repeat/2,1))
    cond_1= np.concatenate((top_pics_stack[0:wm_trial_repeat], bottom_pics_stack[0:wm_trial_repeat], lcue), axis=1) # attractive vs unattractive
    cond_2= np.concatenate((bottom_pics_stack[wm_trial_repeat:wm_trial_repeat*2], top_pics_stack[wm_trial_repeat:wm_trial_repeat*2], lcue), axis=1) # unattractive vs attractive
    cond_3= np.concatenate((bottom_pics_stack[wm_trial_repeat*2:wm_trial_repeat*3], bottom_pics_stack[wm_trial_repeat*3:wm_trial_repeat*4], lcue), axis=1) #unatt vs unatt
    cond_4= np.concatenate((top_pics_stack[wm_trial_repeat*2:wm_trial_repeat*3], top_pics_stack[wm_trial_repeat*3:wm_trial_repeat*4], lcue), axis=1) #att vs att
    stimuli = np.concatenate((cond_1, cond_2, cond_3, cond_4), axis=0)
    #END CREATE STIMULUS INDEX
    
    #stimuli:
    circle = visual.Circle(win, radius=0.32, edges=100, lineColor=(0 , 0, 0), fillColor=(0 , 0, 0), interpolate=True)# radii chosen so that the area of the square and circle are identical
    square = visual.Circle(win, radius=0.4, edges=4, lineColor=(0 , 0, 0), fillColor=(0 , 0, 0)) #idem
    message3 = visual.TextStim(win, pos=[0,2],color=[0,0,0],text='Select in each screen the position (left/right, as relative to yourself) where\
        the circle is located. \n\nIndicate your choice by pressing the left or right arrow keys on the keyboard as rapidly as possible.\
        \n\nPress any key to continue',wrapWidth=20.0)
    image_l = visual.ImageStim(win, name='image',image='sin', mask=None,ori=0, pos=[7.5,0], size=[15,20],color=[1,1,1], colorSpace=u'rgb',
        opacity=1,texRes=128, interpolate=True, depth=0.0, flipVert=True)
    image_r = visual.ImageStim(win, name='image',image='sin', mask=None,ori=0, pos=[-7.5,0], size=[15,20],color=[1,1,1], colorSpace=u'rgb',
        opacity=1,texRes=128, interpolate=True, depth=0.0, flipVert=True)
    core.wait(process_paddingtime,process_paddingtime)

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
            circle.setPos((14.5,0))
            square.setPos((-14.5,0))
        else:
            circle.setPos((-14.5,0))
            square.setPos((14.5,0))
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
        if controller:
            controller.startTracking()
        trialClock.reset() #Put this after the fixation win.flip if you want to count fixation as part of the trial.
        core.wait(att_time,att_time)
        keypress = event.getKeys(keyList=None,timeStamped=trialClock)
        if keypress == []:
            keypress = np.array([['none',2]])
        elif keypress != []:
            keypress = np.array(keypress)
        keypress = keypress[np.in1d(keypress[:, 0], ['left', 'right', 'none'])]#remove any other keys except left, right, none
        if len(keypress) == 0:
            keypress = np.array(['none',2])
        if controller:
            controller.stopTracking()
        wmwriter.writerow([attwm_loop_val['namel'],attwm_loop_val['ratel'],attwm_loop_val['RTl'],
        attwm_loop_val['orderl'],attwm_loop_val['namer'],attwm_loop_val['rater'],attwm_loop_val['RTr'],
        attwm_loop_val['orderr'],attwm_loop_val['stiml'],keypress[0][0], keypress[0][1], ix])
    wmfile.close()
    if eyetracker_do:
        from letobii import TobiiController
        controller.closeDataFile()
    #END INTERACTING W/ PARTICIPANT

def eyetracker(win, expInfo, face_gender, experiment):
    import sys
    from letobii import TobiiController
    eyedata = 'results/' +  expInfo['Identifier'] + '_' + face_gender + '_' + experiment + 'et' + '.tsv'
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
    #END INTERACTING W/ PARTICIPANT
    return controller