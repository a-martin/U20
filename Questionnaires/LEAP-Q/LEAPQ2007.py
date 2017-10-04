# -*- coding: utf-8 -*-

from psychopy import gui, misc, core

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
    
    # print(ok_dlg)

    lg = ok_dlg[0] # fetch langauge info
    cheminT = "./LEAP_text/" + lg + "/" # location of text

    # Basic info
    with open(cheminT + 'basic_info.txt') as f:
        lines = f.readlines()
        dlgQ = gui.Dlg(title=lines[0])
        lines = lines[1:] # extract title line from file
        dbLabels = []

        for l in lines:
            l = l.strip()
            l = l.split(';')
            
            # Fetch question type
            qType = l[0]
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
            dico = {}
            for n,i in enumerate(rep):
                dico[dbLabels[n]] = i

            print dico





    

    # print cheminT

    # nbqs = 5

    # for qnb in range(nbqs):
    #     with open(cheminT + str(qnb) + ".txt") as f:
    #         lines = f.readlines()
    #         dlgQ = gui.Dlg(title=lines[0])
    #         lines = lines[1:] # extract title line from file

    #         for l in lines:
    #             l = l.strip()

    #             if l[0] == '#': # ignore field
    #                 break

    #             elif l[0] == '!': # special question type

    #                 if l[1] == "T": # add text
    #                     l = l.split(';')[1:]
    #                     dlgQ.addText(l[0])
                
    #                 elif l[1] == "X": # multiple choice question
    #                     l = l.split(';')[1:] # remove initial X
    #                     choiceText = l[0]
    #                     choiceFile = l[1]
    #                     ## open file and fetch contents
    #                     with open(cheminT+choiceFile) as cf:
    #                         clines = cf.readlines()
    #                         choix = {}
    #                         for c in clines:
    #                             c = c.strip().split(';')
    #                             choix[c[0]] = c[1]
    #                     dlgQ.addField(l[0], choices=choix.keys())

                        
    #                 elif l[1] == "L": # list multiple answers
    #                     l = l.split(';')
    #                     nbrep = int(l[1])
                       
    #                     dlgQ.addText(l[2])
    #                     for i in range(nbrep):
    #                         dlgQ.addField()

    #                 elif l[1] not in supqs:
    #                     print 'Error. Question type not supported.'

    #             else: # simple input
    #                 dlgQ.addField(l+': ')
                    
    #         rep = dlgQ.show()
            
    #         print rep 

else:
    core.quit()



    










