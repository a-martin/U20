# -*- coding: utf-8 -*-

from psychopy import core, gui, misc, data, visual, event, sound
import pandas as pd
import numpy as np
import codecs # for utf-8 file handling


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
    x = sound.Sound('../stimuli/'+x)
    x.play()
    core.wait(x.getDuration())
    return


def makeButton(buttonName):
    button = visual.Rect(
        win,
        width=buttonWidth,
        height=buttonHeight,
        fillColor=buttonColor,
        pos=buttonPositions[buttonName],
        autoDraw=True
    )
    button.draw()
    return button

    
def doTrial(essaiID, trialsAll):

    trial = trialsAll.ix[essaiID]
    mouse = event.Mouse()
    
    win.flip()
    visual.TextStim(
        win,
        text=trial['displayPhrase'],
        color='black'
    ).draw()
    win.flip()
    playStim(trial['soundFile'])
    # event.waitKeys()

    if trial['type'] == 'training':
        buttonNames = [
            'A',
            'B'
        ]

    elif trial['type'] == 'test':
        buttonNames = [
            'A',
            'B',
            'C',
            'D'
        ]

    else:
        buttonNames = []

    buttons = [makeButton(buttonName) for buttonName in buttonNames]
    
    win.flip()
    # event.waitKeys()

    clicked = False    
    while not clicked:
        for n, button in enumerate(buttons):
            if button.contains(mouse):
                button.setFillColor(hoverColor)
                win.flip()
            else:
                button.setFillColor(buttonColor)
                win.flip()
            if mouse.isPressedIn(button):
                clicked = True
                response = n
                print response




    return

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
if dlg.OK:    if ID == 'adj' or ID == 'num':

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
noms = noms.sample(20)
repeatNoms = noms.sample(10)
noms = pd.concat([noms, repeatNoms])


# Modifiers
mods = pd.read_csv('../stimuli/modifiers.csv')

# condition name contains two modifier types
innerID, outerID = cond.split('-')
IDs = [innerID, outerID]

# create a dict with each mod type as key and associated df (shuffled) as values
inOutSets = {ID:mods[mods.cat==ID].sample(frac=1).reset_index(drop=True) for ID in IDs}

# create correct number of single mod trials depending on mod type
inner, outer = [draw1ModSet(ID, inOutSets[ID]) for ID in IDs]







# BUTTON PARAMETERS

buttonWidth = 280
buttonHeight = 80

buttonPositions = {
    'A': (buttonWidth/2*-1, buttonHeight/2),
    'B': (buttonWidth/2, buttonHeight/2),
    'C': (buttonWidth/2*-1, buttonHeight/2*-1),
    'D': (buttonWidth/2, buttonHeight/2*-1)
}

hoverColor = "grey"
buttonColor = "lightgrey"

#########################




#########################
#### RUN EXPERIMENT ####

# DRAW WINDOW
if plein_ecran:
    win = visual.Window(
        fullscr=True,
        allowGUI=False,
        color="grey",
        colorSpace="rgb",
        units="pix"
    )
else:
    win = visual.Window(
        [800,800],
        color="grey",
        colorSpace="rgb",
        units="pix"
    )
win.flip()


consigne = u'''INSTRUCTIONS.'''
instructies(consigne)

trialsAll = pd.read_csv('tmpTrials.csv', index_col=0)

for essaiID in trialsAll.index:
    doTrial(essaiID, trialsAll)










