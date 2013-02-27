#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
from psychopy import visual, core #import some libraries from PsychoPy

#MONITOR SPECS:
resolution = [1920, 1080]
framerate = 60
print framerate

#TIMES (in [ms]):
fixation = 4000

#calculate times in [frames] instead of [ms]
start = 200
fixation = fixation / (1000 / framerate)

print fixation
#create a window
mywin = visual.Window(resolution,fullscr=True,allowGUI=False,monitor="testMonitor", screen=1, units="deg")
mywin.setRecordFrameIntervals(True)

#create some stimuli
fixation_h = visual.Line(mywin, start=(-0.4, 0.0), end=(0.4, 0.0))
fixation_v = visual.Line(mywin, start=(0.0, -0.4), end=(0.0, 0.4))
gabor = visual.Polygon(mywin)


clock = core.Clock()
#let's draw a stimulus for 2s, drifting for middle 0.5s
for fra in range(int(start+fixation)):#for exactly 200 frames
    if start<=fra<start+fixation:#present fixation for a subset of frames
        fixation_h.draw()
        fixation_v.draw()
    if start<=fra<start+fixation:#present stim for a different subset
        gabor.draw()
    mywin.flip()

print mywin.frameIntervals
#name='/home/chymera/Wip/AG-Humphreys/psychpy/lala.txt'
#open(name, 'w')
#name.write(mywin.frameIntervals)
#name.close()