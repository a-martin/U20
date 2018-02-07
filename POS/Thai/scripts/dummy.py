# -*- coding: utf-8 -*-


from psychopy import core, visual
import os, re, random


chemin = '../stimuli/tha/images/'
files = os.listdir(chemin)
p = re.compile('.*\.png')

win = visual.Window(
    [800,800],
    color="lightgrey",
    colorSpace="rgb",
    units="pix",
)

win.flip()

# myText = u'วลีที่ต้องแปล!'
# myText = u"ปด"
# myText = u"先生を呼んだ学生先生を呼んだ学生"

random.shuffle(files)

for text in files[:20]:
    t = visual.ImageStim(
        win,
        image=chemin+text
    )
    t.draw()
    win.flip()
    core.wait(0.500)

core.quit()


