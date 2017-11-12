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

    
    return response, correct, buttonTexts[0], buttonTexts[1]


def doTraining(nouns, modifiers):

    global trainingDf
    
    i = 0
    while i < 2:
        modifier = modifiers.ix[i]
        modifierWord = modifier.word
        number = modifier.nb
        if number == 'plur':
            nounWord = nouns.ix[i].plur
        else:
            nounWord = nouns.ix[i].sing

        response, correct, buttonA, buttonB = doTrainingTrial(nounWord, modifierWord, i)
        if correct == 1:
            i += 1
        else:
            continue

        dico = {
            'suj':sujet,
            'trial':i,
            'noun':nounWord,
            'modifier':modifierWord,
            'buttonA':buttonA,
            'buttonB':buttonB,
            'response':response,
            'correct':correct
        }
        trial = pd.DataFrame([dico])
        trainingDf = trainingDf.append(trial)
            
    return



def doTestTrial(nTrial, noun, modOuter, modInner=None):

    core.wait(0.5)

    if type(modInner) is str:
        buttonNames = ['A', 'B', 'C', 'D']

        engText = modOuter + ' ' + modInner + ' ' + noun

        prenom1 = modOuter + ' ' + modInner + ' ' + noun
        prenom2 = modInner + ' ' + modOuter + ' ' + noun
        postnom1 = noun + ' ' + modInner + ' ' + modOuter
        postnom2 = noun + ' ' + modOuter + ' ' + modInner
        
        buttonTexts = [prenom1, prenom2, postnom1, postnom2]

        
    else:
        buttonNames = ['A', 'B']

        engText = modOuter + ' ' + noun
    
        prenom = modOuter + ' ' + noun
        postnom = noun + ' ' + modOuter

        buttonTexts = [prenom, postnom]


    random.shuffle(buttonTexts)
   
    mouse, buttons, cons, eng = initializeTrial(
        displayText=engText,
        buttonNames=buttonNames,
        buttonTexts=['-----'] * len(buttonTexts)
    )


    core.wait(1)

    consBisText = "...click on the choice that the speaker would most likely say... ({}/50)".format(nTrial+1)
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

    buttonA = buttonTexts[0]
    buttonB = buttonTexts[1]
    try:
        buttonC = buttonTexts[2]
        buttonD = buttonTexts[3]
    except:
        buttonC = np.nan
        buttonD = np.nan
        
    # activate mouse
    mouse.setVisible(True)
        
    responseButton, response = getClick(mouse, buttons, cons, eng)

    buttons[responseButton][0].setFillColor('blue')
    
    win.flip()
    core.wait(1)
    
    # erase objects
    for button in buttons:
        button[0].setAutoDraw(False)
        button[1].setAutoDraw(False)

    cons.setAutoDraw(False)
    eng.setAutoDraw(False) 
    consBis.setAutoDraw(False)

    
    return response, responseButton, buttonA, buttonB, buttonC, buttonD


def doTest(trials):

    global testDf
    
    for i in range(6): # trials.index
        row = trials.ix[i]
        response, responseButton, buttonA, buttonB, buttonC, buttonD = doTestTrial(i, row.noun, row.outer, row.inner)

        dico = {
            'trial':i,
            'noun':row.noun,
            'modInner':row.inner,
            'modOuter':row.outer,
            'buttonA':buttonA,
            'buttonB':buttonB,
            'buttonC':buttonC,
            'buttonD':buttonD,
            'response':response,
            'responseButton':responseButton
        }
        dico.update(subjInfo)
        
        trial = pd.DataFrame([dico])
        testDf = testDf.append(trial)
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
if dlg.OK:    
    misc.toFile('../data/lastParams.pickle', expInfo)
else:
    core.quit()

    
conds = ['dem-adj', 'dem-num', 'num-adj']
# use subject number to assign condition
cond = conds[int(expInfo['Subject number']) % 3]
print cond


sujet = lg + expInfo['Booth code'] + expInfo['Subject number']
genre = expInfo['Gender']
age = expInfo['Age']


# create dict of subjInfo
subjInfo = {'suj':sujet, 'date':datum, 'gender':genre, 'age':age, 'cond':cond}
    
# data files
trainingFileName = '../data/training/{}.csv'.format(sujet)
trainingCols = [
    'suj',
    'trial',
    'noun',
    'modifier',
    'buttonA',
    'buttonB',
    'response',
    'correct'
]
trainingDf = pd.DataFrame(columns=trainingCols)

testFileName = '../data/test/{}.csv'.format(sujet)
testCols = [
    'suj',
    'gender',
    'age',
    'date',
    'cond',
    'trial',
    'noun',
    'modInner',
    'modOuter',
    'buttonA',
    'buttonB',
    'buttonC',
    'buttonD',
    'response',
    'responseButton'
]
testDf = pd.DataFrame(columns=testCols)



#########################
#########################

# GENERATE TRIALS

# Nouns
noms = pd.read_csv('../stimuli/nouns.csv')

# sample 20 nouns..half will be repeated for training, thus 30 trials
nomsSample = noms.sample(20)
repeatNoms = nomsSample.sample(10)
trainingNoms = pd.concat([nomsSample, repeatNoms]).reset_index(range(30), drop=True)


# Modifiers
mods = pd.read_csv('../stimuli/modifiers.csv')
nums = mods[mods.cat=='num']
dems = mods[mods.cat=='dem']
adjs = mods[mods.cat=='adj']


# condition name contains two modifier types
innerID, outerID = cond.split('-')
IDs = [innerID, outerID]

# create a dict with each mod type as key and associated df (shuffled) as values
inOutSets = {ID:mods[mods.cat==ID].sample(frac=1).reset_index(drop=True) for ID in IDs}

# create correct number of single mod trials depending on mod type
inner, outer = [draw1ModSet(ID, inOutSets[ID]) for ID in IDs]

# sort training modifiers
trainingModifiers = pd.concat([inner['train'], outer['train']]).reset_index(range(30), drop=True)

# sort modifiers for single modifier test trials, two mod trials assigned later
testSingModifiers = pd.concat([inner['test'], outer['test']]).reset_index(range(20), drop=True)

# create empty df to contain test trials
cols = ['noun', 'outer', 'inner']
trials = pd.DataFrame(columns=cols)

# add (20) single modifier trials to df
for mod in testSingModifiers.index:
    row = testSingModifiers.ix[mod]
    nb = row.nb

    noun = noms.ix[noms.sample(1).index[0]][nb]
    modifier = row.word

    trial = pd.DataFrame([{'noun':noun, 'outer':modifier}], columns=cols)
    trials = trials.append(trial, ignore_index=True)

# add (30) two modifier trials to df
for i in range(30):
        
    if cond == 'dem-num':
        # agreement is based on sampled num
        trumpMod = nums.ix[nums.sample(1).index[0]]

        # sample a noun that agrees in nb with num
        noun = noms.ix[noms.sample(1).index[0]][trumpMod.nb]
        modInner = trumpMod.word
        # sample a dem that agrees in nb with num
        modOuter = dems.ix[dems[dems.nb==trumpMod.nb].sample(1).index[0]].word

    elif cond == 'dem-adj':
        # agreement is based on sampled dem
        trumpMod = dems.ix[dems.sample(1).index[0]]

        # sample a noun that agrees in nb with dem
        noun = noms.ix[noms.sample(1).index[0]][trumpMod.nb]
        modOuter = trumpMod.word
        # sample any adjective
        modInner = adjs.ix[adjs.sample(1).index[0]].word
        
    elif cond == 'num-adj':
        # agreement is based on sampled num
        trumpMod = nums.ix[nums.sample(1).index[0]]

        # sample a noun that agrees in nb with num
        noun = noms.ix[noms.sample(1).index[0]][trumpMod.nb]
        modOuter = trumpMod.word
        # sample any adjective
        modInner = adjs.ix[adjs.sample(1).index[0]].word

    # create trial df
    trial = pd.DataFrame([{'noun':noun, 'outer':modOuter, 'inner':modInner}], columns=cols)
    # append trial to all trials df    
    trials = trials.append(trial, ignore_index=True)

# shuffle trials and reset index to be 0-49
trials = trials.sample(frac=1)
trials = trials.reset_index(range(50))

#########################
#########################



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


welcome = u'''Welcome!

This is an experiment about learning a small part of a new language. It will take about 30 minutes to complete and you will be paid £5.00 for your time. This experiment is part of a series of studies being conducted by Dr Jennifer Culbertson at the University of Edinburgh, and has been approved by the Linguistics and English Language Ethics Committee. 

Proceeding indicates that:

- you are a native speaker of English, at least 18 years old
- you have read the information letter
- you voluntarily agree to participate, and understand you can stop your participation at any time
- you agree that your anonymous data may be kept permanently in Edinburgh University archives and may used by qualified researchers for teaching and research purposes

If you do not agree to all of these, please inform the experimenter now.

If you agree, press the spacebar.'''
instructies(welcome)

consigne = u'''In this experiment, you will be learning part of a new language.  The language is similar to English, but you will notice some differences.

Your task will be to learn to translate from English into the new language.

Press the spacebar to continue.
'''
instructies(consigne)

consigne = u'''Instructions -- please read carefully!

Now you'll see a phrase in English, and hear a speaker of the language you're learning translate it.

Look at the English phrase, listen to the speaker translate it, and then click on the translation that matches what you heard the speaker say.

It's important to pay close attention, so that later on you'll be able to translate on your own.

Press the spacebar to continue.
'''
instructies(consigne)


doTraining(trainingNoms, trainingModifiers)
trainingDf.to_csv(trainingFileName, index=False)


testConsigne = u'''Instructions -- please read carefully!

In the next part of the experiment, you will show what you have learned about this new language.

You will see an English phrase -- it may be the SAME LENGTH phrase that you have seen before, or it may be LONGER.

Look at the English phrase, and click on the translation that you think a speaker of the language WOULD BE MOST LIKELY TO SAY.

Try to do as well as you can, remembering what you learned in the first part of the experiment, but don't worry if once in a while you have to guess.

Press the spacebar to continue.
'''
instructies(testConsigne)

doTest(trials)
testDf.to_csv(testFileName, index=False)

end = u'''Thank you!

Please see the experimenter, who will proceed with a questionnaire about your linguistic experience.

Press the spacebar to exit the experiment.
'''
instructies(end)

core.quit()


