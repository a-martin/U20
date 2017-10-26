# -*- coding: utf-8 -*-

from psychopy import core, gui, visual, event
import pandas as pd



### DRAW WINDOW ###
pec = {'Full screen':'y'}
dlg = gui.DlgFromDict(pec, title=u'Démarrage')
if dlg.OK:
    if pec['Full screen'] == 'y':
        plein_ecran = True
    else:
        plein_ecran = False
else:
    core.quit()


    
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

##################

def displayStim(word):
    win.flip()
    core.wait(0.15)
    visual.TextStim(
        win,
        word,
        height=60,
        wrapWidth=1000
    ).draw()
    win.flip()
    pressed = event.waitKeys()
    return pressed

################

nouns = pd.read_csv('nouns.csv')
    
sings = nouns.sing.sample(frac=1)
plurs = nouns.plur.sample(frac=1)


mods = pd.read_csv('modifiers.csv')
mods = mods.word.sample(frac=1)

jenny = pd.read_csv('allNPs.csv')
jenny = jenny.np.sample(frac=1)


"""
Run through:

sings
plurs
mods
jenny

"""


for word in sings:
    pressed = []
    while pressed != ['right']:
        pressed = displayStim(word)
