#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2023.1.3),
    on November 13, 2023, at 13:01
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '3'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard
import pandas as pd
# Run 'Before Experiment' code from code
#PREWRITTEN CODE
# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2023.1.3'
expName = 'DROFunctions'  # from the Builder filename that created this script
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
}
#DROBError, BE stands for Both Error (so combined error).

mySound = sound.Sound("Point.wav")

Duration = 1
dragging = False
xpos = 0.3
xpos2 = -0.3
ypos2 = 0
Order = 0
ypos = 0
ClickVariable = 0
#Initalize timers
DROTimer = core.Clock()
FITimer = core.Clock()
FITimer.addTime(0)
DROTimer.addTime(0)

#Keeps track of how long current phase has been going
PhaseTimer = core.Clock()
PhaseTimer.addTime(0)

PointTimer = core.Clock()
PointTimer.addTime(0)
#keeps track of when last button click was
MouseTimer = core.Clock()
MouseTimer.addTime(0)
#Keeps track of total runtime
RunTimer = core.Clock()
RunTimer.addTime(0)
BreakPauseTime = 0 
PointBoxColor = 0
CircleOn = 1
RedCircleOn = 1
newPhase = True
#Initialize txtboxes
routineended = False
timertxt = "DROTimer"
pointstxt = "Points: 0"
FITimertxt = "FITimer"
points = 0
#Points Data, takes data everytime a point happens
IDstr = expInfo['participant']
filename = _thisDir + os.sep + u'participantdata/' + IDstr + '/'


#Interval Data, takes data on clicks and points every 60 seconds happens, will need to be made to sync up with phases starting and stopping
#interval = data.ExperimentHandler(name='DROIntegrity', dataFileName=filename + 'IntervalData')
#Phase Data, takes data everytime a click or a point happens in each phase
#PhaseData = data.ExperimentHandler(name = 'DROIntegrity', dataFileName =filename + 'PhaseData')
#Raw Data, takes data everytime a point happens, everytime a click happens, everytime a phase chnage happens, everytime an error happens
RawData = data.ExperimentHandler(name = "DROIntegrity", dataFileName = filename + 'RawData')
#Clicks data, Takes data everytime a click happens
click = data.ExperimentHandler(name='DROIntegrity', dataFileName=filename + 'ClicksData')
CurrentPhase = "Initialize"
DataTimer = core.Clock()
DataTimer.addTime(0)

PointIntCounter = 0
ClickIntCounter = 0
PointPhaseCounter = 0
ClickPhaseCounter = 0

#Initialize Functions

#This resets timers inbetween phases.
def ResetAllTimers():
    FITimer.reset()
    DROTimer.reset()
   
    PhaseTimer.reset()

    return


#This function is the one that should be called
#for any DRO functions. It should be called continously in DRO
#Routines in the Each Frame Section of the code, such that
#the code is checking each frame if the timer has hit 3 secon

#Integrity is the percent integrity
#we want the trial to be called at. It should be represented
#as a decimal inbetween 0 and 1. 1 being 100% integrity, and
#.8 being 80% integrity.

def EachFrameChecker(Stage):
    global CircleOn
    global RedCircleOn
    RTime = RunTimer.getTime()
    PTime = PhaseTimer.getTime()
    
    #Changes botton opacity, turning them off during breaks
    if Phase == "Break":
        CircleOn = 0
        RedCircleOn = 0
    #turns them back on after 0.3 second blink from click
    elif MouseTimer.getTime() > 0.3:
        CircleOn = 1
        #only turns red on during reinforcer assessment
        if Phase == "Assessment":
            RedCircleOn = 1
        else: 
            RedCircleOn = 0
    else:
        CircleOn = 0
        RedCircleOn = 0
    #manages the color of the point box, canges it back to grey after 0.8 seconds. 
    if PointTimer.getTime() > 0.8:
        global PointBoxColor
        PointBoxColor = 0
    
    if Phase == "Intervention" and Stage == "Button" and Reinforcement_Schedule == "DRO":
        #Checks to see if DRO timer has hit 3 seconds
        if DROTimer.getTime() > Reinforcement_Variable:
            
            DROTimer.reset()
            #Calculates if an omission error has happened or not.
            #random() returns a random number inbetween 0 and 1.
            numb = random()*100
            
            if numb <= Omission_Integrity:
                PointEarned("DRO",PTime, RTime)
            else: 
                OmissionErrorNoClick(PTime,RTime)
        return
def OmissionErrorNoClick(PTime,RTime):
    TimeStampData(RawData,PTime,RTime)
    RawData.addData("DataType", "DRO Omission Error")
    RawData.nextEntry()
def ComINTError(PTime,RTime):
    TimeStampData(RawData,PTime,RTime)
    RawData.addData("DataType", "DRO ComINT Error")
    RawData.nextEntry()
#def TakeIntervalData(PTime,RTime):
        #global ClickIntCounter
        #global PointIntCounter
        #TimeStampData(interval,PTime,RTime)
        
        #PhaseData.addData("DataTimerStatus", DataTimer.getTime())
        #PhaseData.addData("ClickCounter", ClickIntCounter)
        #PhaseData.addData("PointIntCounter", PointIntCounter)
        
        #PhaseData.nextEntry()
        #ClickIntCounter = 0
        #PointIntCounter = 0
        #DataTimer.reset()
        #return
#This function should be called anytime the button is clicked
#It will be called in the "Mouse Clicked" routines
#Integrity numbers are same as above
def BreakClick():
    global BreakPauseTime
    if PhaseTimer.getTime() > 5: 
        RTime = RunTimer.getTime()
        PTime = PhaseTimer.getTime()
        TimeStampData(RawData,PTime,RTime)
        RawData.addData('DataType', "PhaseChange")
        RawData.nextEntry()
        RunTimer.reset(-1*BreakPauseTime)
        ResetAllTimers()
        return True
def RedClicked():
    if MouseTimer.getTime() > 0.3:
        MouseTimer.reset()
        RTime = RunTimer.getTime()
        PTime = PhaseTimer.getTime()
        newButtonPosition()
        TimeStampData(click,PTime,RTime)
        click.addData('Point earned?', "N/A")
        click.addData('Point Type', "N/A")
        click.addData('Target Type', "Red")
        
        click.nextEntry()
        
        TimeStampData(RawData, PTime, RTime)
        RawData.addData('DataType', 'RedClick')
        RawData.addData('totalpoints', points)
        RawData.nextEntry()
def MouseClicked():
    global ClickIntCounter
    global ClickPhaseCounter
    ClickIntCounter += 1
    ClickPhaseCounter += 1
   
    if MouseTimer.getTime() > 0.3:
        MouseTimer.reset()
        Earned = False
        PointType = "N/A"

        RTime = RunTimer.getTime()
        PTime = PhaseTimer.getTime()

        newButtonPosition()
        if Phase == "BL" or Phase == "Assessment":
            if Reinforcement_Schedule == "FI":
                if FITimer.getTime() > Reinforcement_Variable:
           
                    #HAVE TO GO HERE AND ADD PTIME RTIME
                    PointEarned("FI " + str(Reinforcement_Variable) + " Button Click",PTime,RTime)
                    PointType = "FI " + str(Reinforcement_Variable)
                    Earned = True
                    #Resets timer FI timer whenever it 
                    #is clicked above 3 seconds
                    FITimer.reset()
            if Reinforcement_Schedule == "FI":
                global ClickVariable
                ClickVariable += 1 
                if ClickVariable >= Reinforcement_Variable:
                    PointEarned("FR " + str(Reinforcement_Variable) + "Button Click", PTime,RTime)
                    PointType = "FI " + str(Reinforcement_Variable)

                    Earned = True
                    ClickVariable = 0 
       
        
        if Phase == "Intervention" and Reinforcement_Schedule == "DRO":
            numb = 100*random()
            if numb <= ComINT:
                DROTimer.reset()
            else:
                ComINTError(PTime,RTime)
            num = random()*100
            
            if num > Comission_Integrity:
                PointEarned("Comission Error",PTime,RTime)
                PointType = "Comission Error"
                Earned = True
            
            
        TimeStampData(click,PTime,RTime)
        click.addData('Point earned?', Earned)
        click.addData('Point Type', PointType)
        if Phase == "Assessment":
            click.addData('Target Type', "Target")
        click.nextEntry()
        if Earned != True:
            TimeStampData(RawData, PTime, RTime)
            RawData.addData('DataType', "Click")
            RawData.nextEntry()
        #Anytime button is clicked, DROTimer is reset
        #Right? Ask Paige
        
    
    return

#This is what is actualyl contorlling the expirement, but not for data purposes. 
def RoutineEnder():
    #This ends routine
    
    if PhaseTimer.getTime() > Duration and Phase != "Break":
        global routineended
        #ends loop and routine if it is time to move on
        global PointPhaseCounter
        global ClickPhaseCounter
        RTime = RunTimer.getTime()
        PTime = PhaseTimer.getTime()
        if Phase == "Assessment":
            global points
            global pointstxt
            points = 0
            pointstxt = "Points: " + str(points)
        #TimeStampData(PhaseData,PTime,RTime)
        #PhaseData.addData("PointsEarned", PointPhaseCounter)
        #PhaseData.addData("Clicks", ClickPhaseCounter)
        #PhaseData.nextEntry()
        PointPhaseCounter = 0
        ClickPhaseCounter = 0
        TimeStampData(RawData,PTime,RTime)
        RawData.addData('DataType', "PhaseChange")
        RawData.nextEntry()
    
        
        
        #PRint Loop Ends
        routineended = True
        PhaseTimer.reset()
        ResetAllTimers()
        return True
    return False
#makes new button position, will be called when clicks happen
def newButtonPosition():
    
    global xpos
    global ypos
    global xpos2
    global ypos2
    x = win.size[0]
    y = win.size[1]

    xpos = random()*((x/y)-0.05) - ((x/y)/2) + 0.025
    ypos = (random()*.8) - 0.45
   
    
    xpos2 = random()*((x/y)-0.05) - ((x/y)/2) + 0.025
    ypos2 = (random()*.8) - 0.45
    while ((xpos2 - xpos)**2 + (ypos2 - ypos)**2)**0.5 < 0.1:
        xpos2 = random()*((x/y)-0.05) - ((x/y)/2) + 0.025
        ypos2 = (random()*.8) - 0.45
    

#THIS IS CURRENTLY ONLY FOR DATA PURPOSES
def TimeStampData(File,PTime,RTime):
    #RunTimer is not athing for wahtever reason, fix later
    File.addData('RunTime', RTime)
    
    CPhase = ""
    if Phase == "BL":
        CPhase = "BL"
    elif Phase == "Break":
        CPhase = "Break"
    elif Phase == "Assessment":
        CPhase = "Assessment"
    elif Phase == "Intervention" and Reinforcement_Schedule == "DRO":
        if Comission_Integrity != 100 and Omission_Integrity != 100:
            CPhase = "Combined C" + str(Comission_Integrity) + "/O" + str(Omission_Integrity)
        elif Comission_Integrity != 100:
            CPhase = "DRO Commission " + str(Comission_Integrity)
        elif Omission_Integrity != 100: 
            CPhase = "DRO Omission " + str(Omission_Integrity)
        else: CPhase = "Perfect DRO"
        
        if ComINT < 100: 
            CPhase += " w/ ComINT " + str(ComINT)
        

        
        
        
    File.addData('Current Phase', CPhase) 
    File.addData('PhaseRuntime', PTime)
    
def PointEarned(Type,PTime,RTime):
    global points
    global pointstxt
    global PointBoxColor
    global PointIntCounter
    global PointPhaseCounter
    global mySound
    PointBoxColor =  0.9059
    PointTimer.reset()
    mySound.stop()
    mySound.play() 
    PointIntCounter +=1
    PointPhaseCounter += 1
    points += 1
    pointstxt = "Points: " + str(points)
    #adds data to points file
    #TimeStampData(exp,PTime,RTime)
    #exp.addData('totalpoints', points)
    #exp.addData('ReasonPointEarned', Type)
   
    
    #exp.nextEntry()
    #adds data to raw file about points
    TimeStampData(RawData,PTime,RTime)
    RawData.addData('DataType', "Point")
    RawData.addData('totalpoints', points)
    RawData.addData('ReasonPointedEarned', Type)
    RawData.nextEntry()
    
    return



# --- Show participant info dialog --
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='C:\\Users\\tde\\Desktop\\College\\PsycoPy\\FixStutter\\FixStutter.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# --- Setup the Window ---
win = visual.Window(
    size=[1280, 720], fullscr=True, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    backgroundImage='', backgroundFit='none',
    blendMode='avg', useFBO=True, 
    units='height')
win.mouseVisible = False
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
# --- Setup input devices ---
ioConfig = {}

# Setup iohub keyboard
ioConfig['Keyboard'] = dict(use_keymap='psychopy')

ioSession = '1'
if 'session' in expInfo:
    ioSession = str(expInfo['session'])
ioServer = io.launchHubServer(window=win, **ioConfig)
eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

# --- Initialize components for Routine "Initalize" ---
text = visual.TextStim(win=win, name='text',
    text='Your goal is to earn as many points as possible. How you earn points may change throughout the experiment. All your points will be visible throughout the experiment at the top of the screen. You will be given optional 1-minute breaks every 5 minutes and a 10-minute break halfway through the experiment (after approximately 30 minutes).You may skip past the breaks by clicking the button that appears on the screen. You are competing with other people for the most points; the top three point-earners in the study will win an additional gift card. Do your best to earn the most points!  Click anywhere when you are ready and good luck',
    font='Open Sans', 
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0)
mouse = event.Mouse(win=win)
x, y = [None, None]
mouse.mouseClock = core.Clock() #368908

# --- Initialize components for Routine "DRO" ---
DROCircle = visual.ShapeStim(
    win=win, name='DROCircle',
    size=[1.0, 1.0], vertices='circle',
    ori=0.0, pos=[0,0], anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor='black',
    opacity=1.0, depth=0.0, interpolate=True)
RedCircle = visual.ShapeStim(
    win=win, name='RedCircle',
    size=[1.0, 1.0], vertices='circle',
    ori=0.0, pos=[0,0], anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor=[1.0000, -1.0000, -1.0000],
    opacity=1.0, depth=-1.0, interpolate=True)
DROMouse = event.Mouse(win=win)
x, y = [None, None]
DROMouse.mouseClock = core.Clock()
# Run 'Begin Experiment' code from DROCode
#DROBError, BE stands for Both Error (so combined error).
#reset timers from last expirement? maybe I suppose.
ResetAllTimers()
if Order == 1: 
    RunTimer.reset()



PointsBox = visual.Rect(
    win=win, name='PointsBox',
    width=(2, 0.1)[0], height=(2, 0.1)[1],
    ori=0.0, pos=(0, 0.45), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor=[-1.0000, -1.0000, -1.0000], fillColor='white',
    opacity=None, depth=-3.0, interpolate=True)
DROPoints = visual.TextStim(win=win, name='DROPoints',
    text='',
    font='Open Sans',
    pos=(0, 0.45), height=0.05, wrapWidth=None, ori=0.0, 
    color='black', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-4.0);
BreakTxt = visual.TextStim(win=win, name='BreakTxt',
    text='Break \n' + str(Duration - PhaseTimer.getTime()) + 'If you wish to skip the break, click the orange square below',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=-5.0);
BreakButton = visual.Rect(
    win=win, name='BreakButton',
    width=(0.1, 0.1)[0], height=(0.1, 0.1)[1],
    ori=0.0, pos=(0, -0.3), anchor='center',
    lineWidth=1.0,     colorSpace='rgb',  lineColor='white', fillColor=[1.0000, 0.2941, -1.0000],
    opacity=None, depth=-6.0, interpolate=True)

# --- Initialize components for Routine "End" ---
text_2 = visual.TextStim(win=win, name='text_2',
    text='The experiment is done, please alert the researcher \n Thank you for participating! \n Please alert the researcher',
    font='Open Sans',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0.0, 
    color='white', colorSpace='rgb', opacity=None, 
    languageStyle='LTR',
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine 

# --- Prepare to start Routine "Initalize" ---
continueRoutine = True
# update component parameters for each repeat
# setup some python lists for storing info about the mouse
mouse.x = []
mouse.y = []
mouse.leftButton = []
mouse.midButton = []
mouse.rightButton = []
mouse.time = []
mouse.clicked_name = []
gotValidClick = False  # until a click is received
# keep track of which components have finished
InitalizeComponents = [text, mouse]
for thisComponent in InitalizeComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "Initalize" ---
routineForceEnded = not continueRoutine

while continueRoutine:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text* updates
    
    # if text is starting this frame...
    if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text.frameNStart = frameN  # exact frame index
        text.tStart = t  # local t and not account for scr refresh
        text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text.started')
        # update status
        text.status = STARTED
        text.setAutoDraw(True)
    
    # if text is active this frame...
    if text.status == STARTED:
        # update params
        pass
    # *mouse* updates
    
    # if mouse is starting this frame...
    if mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        mouse.frameNStart = frameN  # exact frame index
        mouse.tStart = t  # local t and not account for scr refresh
        mouse.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(mouse, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.addData('mouse.started', t)
        # update status
        mouse.status = STARTED
        mouse.mouseClock.reset()
        prevButtonState = mouse.getPressed()  # if button is down already this ISN'T a new click
    if mouse.status == STARTED:  # only update if started and not finished!
        buttons = mouse.getPressed()
        if buttons != prevButtonState:  # button state changed?
            prevButtonState = buttons
            if sum(buttons) > 0:  # state changed to a new click
                # check if the mouse was inside our 'clickable' objects
                gotValidClick = False
                clickableList = environmenttools.getFromNames(text, namespace=locals())
                for obj in clickableList:
                    # is this object clicked on?
                    if obj.contains(mouse):
                        gotValidClick = True
                        mouse.clicked_name.append(obj.name)
                x, y = mouse.getPos()
                mouse.x.append(x)
                mouse.y.append(y)
                buttons = mouse.getPressed()
                mouse.leftButton.append(buttons[0])
                mouse.midButton.append(buttons[1])
                mouse.rightButton.append(buttons[2])
                mouse.time.append(mouse.mouseClock.getTime())
                
                continueRoutine = False  # end routine on response
    
    # check for quit (typically the Esc key)
    if (defaultKeyboard.getKeys(keyList=["escape"]) and defaultKeyboard.getKeys(keyList=["right"])) or endExpNow:
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in InitalizeComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "Initalize" ---
for thisComponent in InitalizeComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# Run 'End Routine' code from code
ResetAllTimers()
#Not at all sure what run time is, or if its ever used, leaving in for now becuase why not

# store data for thisExp (ExperimentHandler)
thisExp.addData('mouse.x', mouse.x)
thisExp.addData('mouse.y', mouse.y)
thisExp.addData('mouse.leftButton', mouse.leftButton)
thisExp.addData('mouse.midButton', mouse.midButton)
thisExp.addData('mouse.rightButton', mouse.rightButton)
thisExp.addData('mouse.time', mouse.time)
thisExp.addData('mouse.clicked_name', mouse.clicked_name)
thisExp.nextEntry()
# the Routine "Initalize" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
PhaseSelector = data.TrialHandler(nReps=1.0, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('Script.xlsx'),
    seed=None, name='PhaseSelector')
thisExp.addLoop(PhaseSelector)  # add the loop to the experiment
thisPhaseSelector = PhaseSelector.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisPhaseSelector.rgb)
if thisPhaseSelector != None:
    for paramName in thisPhaseSelector:
        exec('{} = thisPhaseSelector[paramName]'.format(paramName))

for thisPhaseSelector in PhaseSelector:
    currentLoop = PhaseSelector
    # abbreviate parameter names if possible (e.g. rgb = thisPhaseSelector.rgb)
    if thisPhaseSelector != None:
        for paramName in thisPhaseSelector:
            exec('{} = thisPhaseSelector[paramName]'.format(paramName))
    
    # --- Prepare to start Routine "DRO" ---
    continueRoutine = True
    # update component parameters for each repeat
    DROCircle.setSize((0.1, 0.1))
    RedCircle.setSize((0.1,0.1))
    # setup some python lists for storing info about the DROMouse
    DROMouse.x = []
    DROMouse.y = []
    DROMouse.leftButton = []
    DROMouse.midButton = []
    DROMouse.rightButton = []
    DROMouse.time = []
    DROMouse.corr = []
    DROMouse.clicked_name = []
    gotValidClick = False  # until a click is received
    # Run 'Begin Routine' code from DROCode
    if Phase == "Break":
        BreakPauseTime = RunTimer.getTime()
    if Order == 1:
        RunTimer.reset()
        ResetAllTimers()
    # keep track of which components have finished
    DROComponents = [DROCircle, DROMouse, PointsBox, DROPoints, BreakTxt, BreakButton]
    for thisComponent in DROComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "DRO" ---
    routineForceEnded = not continueRoutine
    dragging = False
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *DROCircle* updates
        
        # if DROCircle is starting this frame...
        if DROCircle.status == NOT_STARTED and frameN >= 0:
            # keep track of start time/frame for later
            DROCircle.frameNStart = frameN  # exact frame index
            DROCircle.tStart = t  # local t and not account for scr refresh
            DROCircle.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(DROCircle, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'DROCircle.started')
            # update status
            DROCircle.status = STARTED
            DROCircle.setAutoDraw(True)
        
        # if DROCircle is active this frame...
        if DROCircle.status == STARTED:
            # update params
            DROCircle.setOpacity(CircleOn, log=False)
            DROCircle.setPos((xpos, ypos), log=False)
            DROCircle.setLineColor([0.0000, 0.0000, 0.0000], log=False)
         # *RedCircle* updates
        
        # if RedCircle is starting this frame...
        if RedCircle.status == NOT_STARTED and frameN >= 0:
            # keep track of start time/frame for later
            RedCircle.frameNStart = frameN  # exact frame index
            RedCircle.tStart = t  # local t and not account for scr refresh
            RedCircle.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(RedCircle, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'RedCircle.started')
            # update status
            RedCircle.status = STARTED
            RedCircle.setAutoDraw(True)
        
        # if RedCircle is active this frame...
        if RedCircle.status == STARTED:
            # update params
            RedCircle.setOpacity(RedCircleOn, log=False)
            RedCircle.setPos((xpos2, ypos2), log=False)
            RedCircle.setLineColor([0.0000, 0.0000, 0.0000], log=False)
        # *DROMouse* updates
        # *DROMouse* updates
        
        # if DROMouse is starting this frame...
        if DROMouse.status == NOT_STARTED and t >= 0-frameTolerance:
            # keep track of start time/frame for later
            DROMouse.frameNStart = frameN  # exact frame index
            DROMouse.tStart = t  # local t and not account for scr refresh
            DROMouse.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(DROMouse, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('DROMouse.started', t)
            # update status
            DROMouse.status = STARTED
            prevButtonState = DROMouse.getPressed()  # if button is down already this ISN'T a new click
        if DROMouse.status == STARTED:  # only update if started and not finished!
            buttons = DROMouse.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClidck = False
                    clickableList = environmenttools.getFromNames([DROCircle, RedCircle, BreakButton], namespace=locals())
                    for obj in clickableList:
                        # is this object clicked on?
                        if obj.contains(DROMouse):
                            gotValidClick = True
                            DROMouse.clicked_name.append(obj.name)
                            ###This part of the code calls functions depending on the current phase for clicks,
                            #Mouse click for phases that aren't break, which gets points (sometimes)
                            if Phase != "Break" and obj == DROCircle:
                                MouseClicked()
                            #should end routine if they clikc on the break button, and resume program
                            if Phase == "Break" and obj == BreakButton:
                                if BreakClick() == True:
                                    continueRoutine = False
                            #This happens if the red butotn is clicked during assesmnet phsae
                            if Phase == "Assessment" and obj == RedCircle:
                                RedClicked()
                    # check whether click was in correct object
                    if gotValidClick:
                        corr = 0
                        corrAns = environmenttools.getFromNames([DROCircle,RedCircle, BreakButton], namespace=locals())
                        for obj in corrAns:
                            # is this object clicked on?
                            if obj.contains(DROMouse):
                                corr = 1
                        DROMouse.corr.append(corr)
                    x, y = DROMouse.getPos()
                    DROMouse.x.append(x)
                    DROMouse.y.append(y)
                    buttons = DROMouse.getPressed()
                    DROMouse.leftButton.append(buttons[0])
                    DROMouse.midButton.append(buttons[1])
                    DROMouse.rightButton.append(buttons[2])
                    DROMouse.time.append(globalClock.getTime())
        # Run 'Each Frame' code from DROCode
        
        timertxt = "DRO Timer: " + str(DROTimer.getTime())
        FITimertxt = "FI Timer: " + str(FITimer.getTime())
        
    
        
        #This part of the code make my brian go ??? what goin on here, trying to make it so that you can't drag
        
        #So this is what is being called every frame, meaning that these are two of the three ways in which events happen. 
        if type(Duration) is int:
            #Routine ender is structured this way because the changing of the value "continueRoutine" only works while the code
            #is physically located in the routine that must end. Basically, when you call RoutineEnder() it returns true or false based on if the duration has been passed.
            if RoutineEnder():
            
                continueRoutine = False
        else:
            continueRoutine = False
        EachFrameChecker("Button")
     
        
        
        
        
        
        # *PointsBox* updates
        
        # if PointsBox is starting this frame...
        if PointsBox.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            PointsBox.frameNStart = frameN  # exact frame index
            PointsBox.tStart = t  # local t and not account for scr refresh
            PointsBox.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(PointsBox, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'PointsBox.started')
            # update status
            PointsBox.status = STARTED
            PointsBox.setAutoDraw(True)
        
        # if PointsBox is active this frame...
        if PointsBox.status == STARTED:
            # update params
            PointsBox.setFillColor([0.0000, PointBoxColor, 0.0000], log=False)
        
        # *DROPoints* updates
        
        # if DROPoints is starting this frame...
        if DROPoints.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            DROPoints.frameNStart = frameN  # exact frame index
            DROPoints.tStart = t  # local t and not account for scr refresh
            DROPoints.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(DROPoints, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'DROPoints.started')
            # update status
            DROPoints.status = STARTED
            DROPoints.setAutoDraw(True)
        
        # if DROPoints is active this frame...
        if DROPoints.status == STARTED:
            # update params
            DROPoints.setText(pointstxt, log=False)
        
        # *BreakTxt* updates
        
        # if BreakTxt is starting this frame...
        if BreakTxt.status == NOT_STARTED and Phase == "Break":
            # keep track of start time/frame for later
            BreakTxt.frameNStart = frameN  # exact frame index
            BreakTxt.tStart = t  # local t and not account for scr refresh
            BreakTxt.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(BreakTxt, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'BreakTxt.started')
            # update status
            BreakTxt.status = STARTED
            BreakTxt.setAutoDraw(True)
        
        # if BreakTxt is active this frame...
        if BreakTxt.status == STARTED:
            # update params
            if Duration > PhaseTimer.getTime(): 
                BreakTxt.text='hey you can take a break now! You have ' + str(round(Duration - PhaseTimer.getTime())) + ' seconds left in your break, \n however you can click the button to end it early \n'
            elif Duration < PhaseTimer.getTime():
                BreakTxt.text = 'Click the button to continue'


        
        # *BreakButton* updates
        
        # if BreakButton is starting this frame...
        if BreakButton.status == NOT_STARTED and Phase == "Break" and PhaseTimer.getTime() >= 2:
            # keep track of start time/frame for later
            BreakButton.frameNStart = frameN  # exact frame index
            BreakButton.tStart = t  # local t and not account for scr refresh
            BreakButton.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(BreakButton, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'BreakButton.started')
            # update status
            BreakButton.status = STARTED
            BreakButton.setAutoDraw(True)
        
        # if BreakButton is active this frame...
        if BreakButton.status == STARTED:
            # update params
            pass
        
        # check for quit (typically the Esc key)
        if (defaultKeyboard.getKeys(keyList=["escape"]) and defaultKeyboard.getKeys(keyList=["right"])) or endExpNow:
            core.quit()
            if eyetracker:
                eyetracker.setConnectionState(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in DROComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "DRO" ---
    for thisComponent in DROComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store data for PhaseSelector (TrialHandler)
    PhaseSelector.addData('DROMouse.x', DROMouse.x)
    PhaseSelector.addData('DROMouse.y', DROMouse.y)
    PhaseSelector.addData('DROMouse.leftButton', DROMouse.leftButton)
    PhaseSelector.addData('DROMouse.midButton', DROMouse.midButton)
    PhaseSelector.addData('DROMouse.rightButton', DROMouse.rightButton)
    PhaseSelector.addData('DROMouse.time', DROMouse.time)
    PhaseSelector.addData('DROMouse.corr', DROMouse.corr)
    PhaseSelector.addData('DROMouse.clicked_name', DROMouse.clicked_name)
    # the Routine "DRO" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1.0 repeats of 'PhaseSelector'

# get names of stimulus parameters
if PhaseSelector.trialList in ([], [None], None):
    params = []
else:
    params = PhaseSelector.trialList[0].keys()
# save data for this loop
PhaseSelector.saveAsExcel(filename + '.xlsx', sheetName='PhaseSelector',
    stimOut=params,
    dataOut=['n','all_mean','all_std', 'all_raw'])

# --- Prepare to start Routine "End" ---
continueRoutine = True
# update component parameters for each repeat
# keep track of which components have finished
EndComponents = [text_2]
for thisComponent in EndComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "End" ---
routineForceEnded = not continueRoutine
routineTimer.reset()
while continueRoutine and routineTimer.getTime() < 300.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text_2* updatesiit d
    
    # if text_2 is starting this frame...
    if text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text_2.frameNStart = frameN  # exact frame index
        text_2.tStart = t  # local t and not account for scr refresh
        text_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text_2, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'text_2.started')
        # update status
        text_2.status = STARTED
        text_2.setAutoDraw(True)
    
    # if text_2 is active this frame...
    if text_2.status == STARTED:
        # update params
        pass
    
    # if text_2 is stopping this frame...
    #if text_2.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        #if tThisFlipGlobal > text_2.tStartRefresh + 200-frameTolerance:
            # keep track of stop time/frame for later
           # #text_2.tStop = t  # not accounting for scr refresh
            #text_2.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            #thisExp.timestampOnFlip(win, 'text_2.stopped')
            # update status
            #text_2.status = FINISHED
            #text_2.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if (defaultKeyboard.getKeys(keyList=["escape"]) and defaultKeyboard.getKeys(keyList=["right"])) or endExpNow:
        core.quit()
        if eyetracker:
            eyetracker.setConnectionState(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        #routineForceEnded = True
        break
    continueRoutine = True  # will revert to True if at least one component still running
    for thisComponent in EndComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "End" ---
print("Program Ended Normally")
for thisComponent in EndComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-20.000000)

# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
