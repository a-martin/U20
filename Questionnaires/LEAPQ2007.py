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


dlg = gui.Dlg(title="Language selection")
# dlg.addField('Test', 'test')
dlg.addField('Language: ', choices=lgs)
ok_dlg = dlg.show() # display dlg and select lg, returns list

if dlg.OK:
    # RUN QUESTIONNAIRE
    
    # print(ok_dlg)

    lg = ok_dlg[0] # fetch langauge info
    cheminT = "./LEAP_text/" + lg + "/" # location of text

    # print cheminT

    nbqs = 5

    for qnb in range(nbqs):
        with open(cheminT + str(qnb) + ".txt") as f:
            lines = f.readlines()
            dlgQ = gui.Dlg(title=lines[0])
            lines = lines[1:] # extract title line from file

            for l in lines:
                l = l.strip()

                if l[0] == '!': # special question type
                
                    if l[1] == "X": # multiple choice question
                        l = l.split(';')[1:] # remove initial X
                        dlgQ.addField(l[0]+': ', choices=l[1:])

                    elif l[1] == "L": # list multiple answers
                        l = l.split(';')
                        nbrep = int(l[1])
                       
                        dlgQ.addText(l[2])
                        for i in range(nbrep):
                            dlgQ.addField()

                    elif l[1] not in supqs:
                        print 'Error. Question type not supported.'

                else: # simple input
                    dlgQ.addField(l+': ')
                    
            rep = dlgQ.show()
            print(rep)

else:
    core.quit()



    










