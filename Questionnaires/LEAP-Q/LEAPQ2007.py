# -*- coding: utf-8 -*-

from psychopy import gui, misc, core
import pandas as pd
from numpy import nan

#####

def fetchRep(dlg, dbLabels):
    global dico
    rep = dlg.show()

    for n,i in enumerate(rep):
        dico[dbLabels[n]] = i
    print dico
    return rep    

def displayQuestion(chemin, questionFile):
    global dico
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
                # rep = dlgQ.show()
                # print rep

                
            elif qType == 'x': # drop-down choice quesiton
                choiceFile = l[3] # these questions should have an additional field with filename
                choix = {}
                # fill dico with choices from choiceFile
                with open(cheminT + choiceFile) as xf:
                    choiceLines = xf.readlines()
                    for choice in choiceLines:
                        choice = choice.strip().split(';')
                        choix[choice[1]] = choice[0]
                        
                # print choix
                dlgQ.addField(
                    label=displayLabel,
                    choices=choix.keys()
                )
                # rep = dlgQ.show()
                # print rep

            elif qType == 'p': # % answers based on previous answers, requires dico to have content
                print displayLabel
                displayLabel = dico[displayLabel]
                if displayLabel != '':
                    dlgQ.addField(label=displayLabel)

                # rep = dlgQ.show()

                
                # break
        fetchRep(dlgQ, dbLabels)


        # rep = dlgQ.show()
        # print rep    

        # if len(rep) == len(dbLabels):
            # print "OK!"
            # dico = {}
        # for n,i in enumerate(rep):
        #     dico[dbLabels[n]] = i
            
        # print dico

        # else:
        #     print "ERROR"
        return





#####

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

cols = list(pd.read_csv('columns.csv'))

# CHOOSE LANGUAGE
dlg = gui.Dlg(title="Language selection")
dlg.addField('Language: ', choices=lgs)
dlg.addField('Subject number: ')
ok_dlg = dlg.show() # display dlg and select lg, returns list

if dlg.OK:
    # RUN QUESTIONNAIRE
    
    lg = ok_dlg[0] # fetch langauge info
    sujet = ok_dlg[1] # fetch subject number


    # df = pd.DataFrame(columns=cols)
    # tmp = pd.Series([nan]*len(cols), index=cols)
    # df.append(tmp, index=sujet)
    
    cheminT = "./LEAP_text/" + lg + "/" # location of text

    dico = {}

    

    # Basic info
    # displayQuestion(cheminT, 'basic_info.txt')
    
    # Language questions
    qs = range(5)

    for q in qs:
        qFile = 'q' + str(q) + '.txt'
        displayQuestion(cheminT, qFile)
            


else:
    core.quit()

allData = pd.read_csv('quest_data.csv', index_col=0)


    










