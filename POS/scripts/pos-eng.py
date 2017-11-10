# -*- coding: utf-8 -*-

from psychopy import core, gui, misc, data, visual, event, sound
import pandas as pd
import numpy as np
import codecs # for utf-8 file handling
import random


#########################
## FUNCTION DEFINITIONS ##

def draw1ModSet(ID, df):
    if ID != 'dem':
        train = pd.concat([df.sample(5)] * 3)
        test = df.copy()
    elif ID == 'dem':
        # repeat four times and drop one line
        train = pd.concat([df] * 4)[:15]
        # repeat three times and drop two lines
        test = pd.concat([df] * 3)[:10]

    return {'train': train, 'test': test}


def commas(x):
    'Turn list into comma-separated string.'
    form = [str(i) for i in x]
    return ','.join(form)
    

def instructies(x):
    'Display instructions on screen and wait for participant to press button'
    win.flip()
    visual.TextStim(win, text=x, color="black", wrapWidth=800).draw()
    win.flip()
    event.waitKeys()
    win.flip()
    return


def playStim(x):
    x.play()
    core.wait(x.getDuration())
    return


def makeButton(buttonName, buttonText):
    button = visual.Rect(
        win,
        width=buttonWidth,
        height=buttonHeight,
        fillColor=buttonColor,
        pos=buttonPositions[buttonName],
        autoDraw=True
    )
    button.draw()

    text = visual.TextStim(
        win,
        text=buttonText,
        color="black",
        pos=buttonPositions[buttonName],
    )
    # textstim does not have autodraw as attribute before creation
    text.setAutoDraw(True)
    text.draw()
    
    return button, text

    
def getClick(mouse, buttons, cons, eng):
    
    clicked = False
    while not clicked:
        # button is a tuple where 0 is shape obj and 1 is text obj
        for n, button in enumerate(buttons):
            if button[0].contains(mouse):
                button[0].setFillColor(hoverColor)
                win.flip()
            else:
                button[0].setFillColor(buttonColor)
                win.flip()
            if mouse.isPressedIn(button[0]):
                clicked = True
                responseButton = n
                # print response

    responseText = buttons[responseButton][1]
                
   
        
    win.flip()
    
    return responseButton, responseText.text
    
    
def initializeTrial(displayText, buttonNames, buttonTexts):

    mouse = event.Mouse(visible=False)
    
    win.flip()

   
    # draw text stimulus and consigne
    cons = visual.TextStim(
        win,
        text="Phrase to be translated:",
        color="black",
        pos=(0,260),
        height=16
    )
    cons.setAutoDraw(True)
    cons.draw()
    
    eng = visual.TextStim(
        win,
        text=displayText,
        color='black',
        pos=(0,200),
        height=36
    )
    eng.setAutoDraw(True)
    eng.draw()
    
    # create button objects (they will keep drawing themselves until turned off)
    buttonsAssc = {}
    for n,i in enumerate(buttonNames):
        buttonsAssc[i] = buttonTexts[n]

    buttons = [makeButton(location, buttonsAssc[location]) for location in buttonsAssc.keys()]
        
        
    win.flip()
    
    return mouse, buttons, cons, eng
    
    
def makePhrase(words):

    stimulus = [sound.Sound('../stimuli/'+i+'-trim.wav') for i in words]

    return stimulus
    


def doTrainingTrial(noun, modifier, nTrial):

    core.wait(0.5)
    
    engText = modifier + ' ' + noun
    prenom = modifier + ' ' + noun
    postnom = noun + ' ' + modifier

    buttonTexts = [prenom, postnom]
    random.shuffle(buttonTexts)
   
    mouse, buttons, cons, eng = initializeTrial(
        displayText=engText,
        buttonNames=['A', 'B'],
        buttonTexts=['-----'] * len(buttonTexts)
    )

    # sound
    stims = makePhrase([noun, modifier])
    for stim in stims:
        playStim(stim)

    core.wait(0.5)

    consBisText = "...click on the choice that matches what you heard... ({}/30)".format(nTrial+1)
    consBis = visual.TextStim(
        win,
        text=consBisText,
        pos=(0,125),
        color="black",
        height=16,
        italic=True
    )
    consBis.setAutoDraw(True)
    win.flip()
    
    # update button text from dashes to actual content
    for n,button in enumerate(buttons):
        button[1].text = buttonTexts[n]
        
    # activate mouse
    mouse.setVisible(True)
        
    responseButton, response = getClick(mouse, buttons, cons, eng)
    # print response
    if response == postnom:
        correct = 1
    else:
        correct = 0

    print correct

    if correct == 1:
        buttons[responseButton][0].setFillColor('green')
    else:
        buttons[responseButton][0].setFillColor('red')

    win.flip()
    core.wait(1)
    
    # erase objects
    for button in buttons:
        button[0].setAutoDraw(False)
        button[1].setAutoDraw(False)

    cons.setAutoDraw(False)
    eng.setAutoDraw(False) 
    consBis.setAutoDraw(False)

    
    return response, correct


def doTraining(nouns, modifiers):

    i = 0
    while i < 5:
        modifier = modifiers.ix[i]
        modifierWord = modifier.word
        number = modifier.nb
        if number == 'plur':
            nounWord = nouns.ix[i].plur
        else:
            nounWord = nouns.ix[i].sing

        response, correct = doTrainingTrial(nounWord, modifierWord, i)
        if correct == 1:
            i += 1
        else:
            continue
    
    return



def doTestTrial(noun, modifier, nTrial):

    core.wait(0.5)
    
    engText = modifier + ' ' + noun
    prenom = modifier + ' ' + noun
    postnom = noun + ' ' + modifier

    buttonTexts = [prenom, postnom]
    random.shuffle(buttonTexts)
   
    mouse, buttons, cons, eng = initializeTrial(
        displayText=engText,
        buttonNames=['A', 'B'],
        buttonTexts=['-----'] * len(buttonTexts)
    )

    # sound
    stims = makePhrase([noun, modifier])
    for stim in stims:
        playStim(stim)

    core.wait(0.5)

    consBisText = "...click on the choice that matches what you heard... ({}/30)".format(nTrial+1)
    consBis = visual.TextStim(
        win,
        text=consBisText,
        pos=(0,125),
        color="black",
        height=16,
        italic=True
    )
    consBis.setAutoDraw(True)
    win.flip()
    
    # update button text from dashes to actual content
    for n,button in enumerate(buttons):
        button[1].text = buttonTexts[n]
        
    # activate mouse
    mouse.setVisible(True)
        
    responseButton, response = getClick(mouse, buttons, cons, eng)
    # print response
    if response == postnom:
        correct = 1
    else:
        correct = 0

    print correct

    if correct == 1:
        buttons[responseButton][0].setFillColor('green')
    else:
        buttons[responseButton][0].setFillColor('red')

    win.flip()
    core.wait(1)
    
    # erase objects
    for button in buttons:
        button[0].setAutoDraw(False)
        button[1].setAutoDraw(False)

    cons.setAutoDraw(False)
    eng.setAutoDraw(False) 
    consBis.setAutoDraw(False)

    
    return response, correct








    
#########################









#########################
## RUNNING PARAMETERS ##

pec = {'Full screen':'y'}
dlg = gui.DlgFromDict(pec, title=u'Démarrage')
if dlg.OK:
    if pec['Full screen'] == 'y':
        plein_ecran = True
    else:
        plein_ecran = False
else:
    core.quit()

#########################






#########################
# SET UP OF EXPERIMENT #
    
# Start parameters
try:
    expInfo = misc.fromFile('../data/lastParams.pickle')
except:
    expInfo = {
        'Subject number':'001',
        'Booth code':'0',
        'Gender':'X',
        'Age':0,
    }

lg = 'ENG'
datum = data.getDateStr(format="%Y-%m-%d %H:%M")

# dialogue box
dlg = gui.DlgFromDict(expInfo, title='Start parameters')
if dlg.OK:    
    misc.toFile('../data/lastParams.pickle', expInfo)
else:
    core.quit()

    
conds = ['adj-dem', 'num-dem', 'adj-num']
# use subject number to assign condition
cond = conds[int(expInfo['Subject number']) % 3]
print cond


sujet = lg + expInfo['Booth code'] + expInfo['Subject number']
genre = expInfo['Gender']
age = expInfo['Age']


# create comma-separated string of subjInfo
subjInfo = commas([sujet, datum, genre, age, cond])
    
# data file
fileName = '../data/{}.csv'.format(sujet)
dataFile = codecs.open(fileName, 'w+', encoding='utf-8')


# GENERATE TRIALS

# Nouns
noms = pd.read_csv('../stimuli/nouns.csv')

# sample 20 nouns..half will be repeated, thus 30 trials
nomsSample = noms.sample(20)
repeatNoms = nomsSample.sample(10)
trainingNoms = pd.concat([nomsSample, repeatNoms]).reset_index(range(30), drop=True)


# Modifiers
mods = pd.read_csv('../stimuli/modifiers.csv')

# condition name contains two modifier types
innerID, outerID = cond.split('-')
IDs = [innerID, outerID]

# create a dict with each mod type as key and associated df (shuffled) as values
inOutSets = {ID:mods[mods.cat==ID].sample(frac=1).reset_index(drop=True) for ID in IDs}

# create correct number of single mod trials depending on mod type
inner, outer = [draw1ModSet(ID, inOutSets[ID]) for ID in IDs]

trainingModifiers = pd.concat([inner['train'], outer['train']]).reset_index(range(30), drop=True)

testModifiers = pd.concat([inner['test'], outer['test']]).reset_index(range(20), drop=True)




# BUTTON PARAMETERS

buttonWidth = 280
buttonHeight = 80

buttonPositions = {
    'A': (buttonWidth/2*-1, buttonHeight/2),
    'B': (buttonWidth/2, buttonHeight/2),
    'C': (buttonWidth/2*-1, buttonHeight/2*-1),
    'D': (buttonWidth/2, buttonHeight/2*-1)
}

hoverColor = "#C0C0C0"
buttonColor = "lightgrey"

#########################




#########################
#### RUN EXPERIMENT ####

# DRAW WINDOW
if plein_ecran:
    win = visual.Window(
        fullscr=True,
        allowGUI=False,
        color="lightgrey",
        colorSpace="rgb",
        units="pix"
    )
else:
    win = visual.Window(
        [800,800],
        color="lightgrey",
        colorSpace="rgb",
        units="pix"
    )
win.flip()


consigne = u'''INSTRUCTIONS.'''
instructies(consigne)


doTraining(trainingNoms, trainingModifiers)




trainingOver = u'''Félicitations !'''
instructies(trainingOver)



