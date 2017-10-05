# -*- coding: utf-8 -*-

from psychopy import gui, misc, core

#####

def displayQuestion(chemin, questionFile):
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
                dlgQ.addField(l[2] + ': ')
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

        rep = dlgQ.show()
        # print rep    

        if len(rep) == len(dbLabels):
            print "OK!"
            # dico = {}
            for n,i in enumerate(rep):
                dico[dbLabels[n]] = i

            print dico

        else:
            print "ERROR"
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

# CHOOSE LANGUAGE
dlg = gui.Dlg(title="Language selection")
# dlg.addField('Test', 'test')
dlg.addField('Language: ', choices=lgs)
ok_dlg = dlg.show() # display dlg and select lg, returns list

if dlg.OK:
    # RUN QUESTIONNAIRE
    
    lg = ok_dlg[0] # fetch langauge info
    cheminT = "./LEAP_text/" + lg + "/" # location of text

    dico = {}

    # Basic info
    displayQuestion(cheminT, 'basic_info.txt')
    
    # Language questions
    qs = range(2)

    for q in qs:
        qFile = 'q' + str(q) + '.txt'
        displayQuestion(cheminT, qFile)
            


else:
    core.quit()



    










