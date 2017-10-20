# -*- coding: utf-8 -*-

from psychopy import gui, misc, core
import pandas as pd
from numpy import nan

####################

def translate(x):
    '''
    Simply return the translation for x if in translation dictionary.
    '''

    if x != '':
        return iso.ix[x]['LanguageName']
    else:
        return x

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
    # print dico
    return rep    

def displayQuestion(chemin, questionFile, n='', language=''):
    '''
    Open a question file and generate dialogue box with content.
    If it is a question related to a specific language, store data with
    n tag (the order of dominance) and display the language name.
    '''

    global dico
    global trad

    # if lg-spec question, append the dominance order to db variable
    if n != '':
        n = '_lg' + n
    
    with open(chemin + questionFile) as f:
        lines = f.readlines()
        dlgQ = gui.Dlg(title=lines[0]) # make dialogue box title first line of file
        lines = lines[1:] # extract title line from file
        dbLabels = []

        for l in lines: # run through other lines of file
            l = l.strip() # remove trailing whitespace
            l = l.split(';') # parse line

            # Fetch question type
            qType = l[0] # first cell is question type

            if qType == 'PROMPT': # simply display text
                dlgQ.addText(l[1].format(language)) # attempt to add lg
                continue

            dbLabel = l[1]+n # name of variable in db
            dbLabels.append(dbLabel)
            displayLabel = l[2].format(language) # text displayed to participant (in lg)

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
                        trad[choice[1]] = choice[0]
                        if choice[0] not in strNos and choice[0] not '':
                            trad[choice[0]] = choice[1]
                        
                        
                dlgQ.addField(
                    label=displayLabel,
                    choices=displayOptions
                )

            elif qType == 'p': # % answers based on previous answers, requires dico to have content

                displayLabel = translate(dico[displayLabel]) # convert ISO to lg name
                
                if displayLabel != '':
                    dlgQ.addField(label=displayLabel)
                # If no lg to treat, should leave final column empty

        fetchRep(dlgQ, dbLabels)

        return
        
def doLgQ(chemin, language, n):
    '''
    For language, display and record series of questions about the acquisition and use of language.
    '''

    global dico
    global trad

    # if no language is stored, then move on to next part of questionnaire
    if language == '':
        return
    
    lgDisplay = translate(language)

    # Prompt
    with open(cheminT+'lg-prompt.txt') as f:
         lines = f.readlines()
         dlgPrompt = gui.Dlg(title=lgDisplay)
         prompt = lines[0].format(lgDisplay)
         dlgPrompt.addText(prompt)
         dlgPrompt.show()

    # text files that contain different questions about lg use
    aspects = [
        'ages.txt',
        'years.txt',
        'proficiency.txt',
        'contributions.txt',
        'expo.txt',
        'accent.txt',
        'accent-id.txt'
    ]

    for aspect in aspects:
        displayQuestion(cheminT, aspect, n, lgDisplay)     
    
    return
    
    


####################

'''
Langauge codes:

English / ENG
Kitharaka / THK
Thai / THA
Vietnamese / VIE

'''

# choices for lg to complete the questionnaire in
displayLgs = [
    'ENG',
    # 'THA',
    # 'VIE',
    # 'THK'
]

strNos = [str(i) for i in range(10)]

# CHOOSE LANGUAGE
dlg = gui.Dlg(title="Language selection")
dlg.addField('Language: ', choices=displayLgs)
dlg.addField('Subject number: ')
ok_dlg = dlg.show() # display dlg and select lg, returns list

if dlg.OK:

    # RUN QUESTIONNAIRE
    
    # Initialize langauge and subject info
    lg = ok_dlg[0] # fetch langauge info
    noSujet = ok_dlg[1] # fetch subject number
    codeSujet = lg + str(noSujet) # final suj no will be p ex ENG0001

    dataFile = 'data/' + codeSujet + '.csv'
        
    # Initialize df with all column names and make 'sujet' index col
    df = pd.read_csv('columns.csv', index_col='sujet') 
    
    cheminT = "./LEAP_text/" + lg + "/" # location of text files
    iso = pd.read_csv(cheminT + 'lgs.csv', sep=';', keep_default_na=False)
    iso = iso.set_index('ISOCAPS')

    dico = {}
    dico['lg'] = lg
    trad = {}

    # WELCOME
    welcomePromptF = cheminT + 'welcome.txt'
    displayPrompt(welcomePromptF)
    
    # PART ONE
    qs = [
        'q0.txt', # basic info, name, etc
        'q1.txt', # dominant languages (REQUIRED)
        'q2.txt', # order of acquisition
        'q3.txt', # langauge use
        'q4.txt', # reading preferences
        'q5.txt', # speaking preferences
        # 'q6.txt', # culture
        'q7.txt', # education
    ]

    
    for q in qs:
        displayQuestion(cheminT, q)

    # PART TWO
    # Fetch participant's reported lgs in order of dominance
    lgs = [
        dico['dom_lg_1'],
        dico['dom_lg_2'],
        dico['dom_lg_3'],
        dico['dom_lg_4'],
        dico['dom_lg_5'],
    ]

    # DISPLAY TRANSITION TEXT TO PART TWO
    transitionPromptF = cheminT + 'transition.txt'
    displayPrompt(transitionPromptF)

      
    for n,langue in enumerate(lgs):
        doLgQ(cheminT, langue, str(n+1))


    
    # SAVE DATA
    # Recover responses from dico and put them into df
    rep = pd.DataFrame(dico, index=[codeSujet])
    rep.index.rename('sujet', inplace=True)

    df = df.append(rep)
    df.to_csv(dataFile)

    # DISPLAY ENDING TEXT
    endPromptF = cheminT + 'fin.txt'
    displayPrompt(endPromptF)

    core.quit()
    
else:
    core.quit()



    
