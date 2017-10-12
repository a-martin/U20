# -*- coding: utf-8 -*-

from psychopy import gui, misc, core
import pandas as pd
from numpy import nan

####################

def translate(x):
    '''
    Simply return the translation for x if in translation dictionary.
    '''

    global trad
    
    if x in trad.keys():
        return trad[x]
    else:
        print "No translation yet available for this item."

def displayPrompt(promptFile):
    '''
    Display a prompt from a text file.
    '''

    with open(promptFile) as f:
        lines = f.readlines()
        dlgP = gui.Dlg(title=lines[0])
        lines = lines[1:] # extract title line from file

        for l in lines:
            l = l.strip()
            dlgP.addText(l)

    dlgP.show()
            
    return 
            
def fetchRep(dlg, dbLabels):
    '''
    Receive input from user and store answer with correct (lg-independent) label for db.
    '''

    global dico
    global trad
    
    rep = dlg.show()

    for n,i in enumerate(rep):
        if i in trad.keys():
            dico[dbLabels[n]] = trad[i]
        else:
            dico[dbLabels[n]] = i
    print dico
    return rep    

def displayQuestion(chemin, questionFile):
    '''
    Open a question file and generate dialogue box with content.
    '''

    global dico
    global trad

    with open(chemin + questionFile) as f:
        lines = f.readlines()
        dlgQ = gui.Dlg(title=lines[0])
        lines = lines[1:] # extract title line from file
        dbLabels = []

        for l in lines:
            l = l.strip()
            l = l.split(';')

            # Fetch question type
            qType = l[0]

            if qType == 'PROMPT': # simply display text
                dlgQ.addText(l[1])
                continue

            dbLabel = l[1] # name of variable in db
            dbLabels.append(dbLabel)
            displayLabel = l[2] # text displayed to participant (in lg)

            if qType == 't': # free text input
                dlgQ.addField(displayLabel + ': ')
                
            elif qType == 'x': # drop-down choice quesiton
                choiceFile = l[3] # these questions should have an additional field with filename
                # fill dico with choices from choiceFile
                with open(cheminT + choiceFile) as xf:
                    choiceLines = xf.readlines()
                    displayOptions = []

                    for choice in choiceLines:
                        choice = choice.strip().split(';')
                        displayOptions.append(choice[1])
                        
                        # Create translation pair in choix dict
                        trad[choice[0]] = choice[1]
                        trad[choice[1]] = choice[0]
                        
                        
                dlgQ.addField(
                    label=displayLabel,
                    choices=displayOptions
                )

            elif qType == 'p': # % answers based on previous answers, requires dico to have content

                displayLabel = translate(dico[displayLabel])
                
                if displayLabel != '':
                    dlgQ.addField(label=displayLabel)
                # If no lg to treat, should leave final column empty

        fetchRep(dlgQ, dbLabels)

        return
        
def doLgQ(chemin, language):
    '''
    For language, display and record series of questions about the acquisition and use of language.
    '''

    global dico
    global trad

    if language == '':
        return
    
    lgDisplay = translate(language)
    
    with open(cheminT+'lg-prompt.txt') as f:
         lines = f.readlines()
         dlgPrompt = gui.Dlg(title=lgDisplay)
         prompt = lines[0].format(lgDisplay)
         dlgPrompt.addText(prompt)
         dlgPrompt.show()

 

    return
    


####################

'''
Langauge codes:

English / ENG
Kitharaka / THK
Thai / THA
Vietnamese / VIE

'''

lgs = [
    'ENG',
    'THA',
    'VIE',
    'THK'
]

supqs = ['X', 'L']

# cols = list(pd.read_csv('columns.csv'))

# CHOOSE LANGUAGE
dlg = gui.Dlg(title="Language selection")
dlg.addField('Language: ', choices=lgs)
dlg.addField('Subject number: ')
ok_dlg = dlg.show() # display dlg and select lg, returns list

if dlg.OK:
    # RUN QUESTIONNAIRE
    # Initialize langauge and subject info
    lg = ok_dlg[0] # fetch langauge info
    noSujet = ok_dlg[1] # fetch subject number
    codeSujet = lg + str(noSujet) # final suj no will be p ex ENG0001

    dataFile = 'data/' + codeSujet + '.csv'

    
    # initialize df with all column names and make 'sujet' index col
    df = pd.read_csv('columns.csv', index_col='sujet') 
    
    cheminT = "./LEAP_text/" + lg + "/" # location of text

    dico = {}
    dico['lg'] = lg
    trad = {}

    # PART ONE
    qs = range(2)

    for q in qs:
        qFile = 'q' + str(q) + '.txt'
        displayQuestion(cheminT, qFile)

    # PART TWO
    # Fetch participant's reported lgs in order of dominance
    lgs = [
        dico['dom_lg_1'],
        dico['dom_lg_2'],
        dico['dom_lg_3'],
        dico['dom_lg_4'],
        dico['dom_lg_5'],
    ]

    print lgs

    transitionPromptF = cheminT + 'transition.txt'
    displayPrompt(transitionPromptF)

      
    for langue in lgs:
        doLgQ(cheminT, langue)


    
    # SAVE DATA
    # recover responses from dico and put them into df
    rep = pd.DataFrame(dico, index=[codeSujet])
    rep.index.rename('sujet', inplace=True)

    df = df.append(rep)
    df.to_csv(dataFile)
    
else:
    core.quit()



    










