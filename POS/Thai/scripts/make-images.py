# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pandas as pd
import matplotlib.pylab as plt


##########

def createImage(english, thai, w, h):

    fileName = outputChemin + english + '.png'

    f = plt.figure()
    f.set_size_inches(w, h)
    
    plt.suptitle(thai, **font)

    plt.savefig(fileName, transparent=True, bbox_inches="tight", dpi=dpi)
    return

##########


dpi = 227.0
buttonWidth = 280
buttonHeight = 80
font = {'fontname':'Silom', 'fontsize':10}

df = pd.read_csv("../stimuli/tha/vocab.csv", index_col=0)
outputChemin = "../stimuli/tha/images/"


nouns = df[df.category=='noun']
mods = df[df.category!='noun']
dems = df[df.category=='dem']
nums = df[df.category=='num']
adjs = df[df.category=='adj']

d = {}

# single modifiers
for mod in mods.index:
    for noun in nouns.index:
        d[mod + noun] = mods.ix[mod].tha.decode('utf-8') + nouns.ix[noun].tha.decode('utf-8')
        d[noun + mod] = nouns.ix[noun].tha.decode('utf-8') + mods.ix[mod].tha.decode('utf-8')

# dem-adj
for dem in dems.index:
    for adj in adjs.index:
        for noun in nouns.index:
            preIsoPhrase = dems.ix[dem].tha.decode('utf-8') + adjs.ix[adj].tha.decode('utf-8') + nouns.ix[noun].tha.decode('utf-8')
            d[dem + adj + noun] = preIsoPhrase
            preNonPhrase = adjs.ix[adj].tha.decode('utf-8') + dems.ix[dem].tha.decode('utf-8') + nouns.ix[noun].tha.decode('utf-8')
            d[adj + dem + noun] = preNonPhrase
            postIsoPhrase = nouns.ix[noun].tha.decode('utf-8') + adjs.ix[adj].tha.decode('utf-8') + dems.ix[dem].tha.decode('utf-8')
            d[noun + adj + dem] = postIsoPhrase
            postNonPhrase = nouns.ix[noun].tha.decode('utf-8') + dems.ix[dem].tha.decode('utf-8') + adjs.ix[adj].tha.decode('utf-8')
            d[noun + dem + adj] = postNonPhrase

# dem-num
for dem in dems.index:
    for num in nums.index:
        for noun in nouns.index:
            preIsoPhrase = dems.ix[dem].tha.decode('utf-8') + nums.ix[num].tha.decode('utf-8') + nouns.ix[noun].tha.decode('utf-8')
            d[dem + num + noun] = preIsoPhrase
            preNonPhrase = nums.ix[num].tha.decode('utf-8') + dems.ix[dem].tha.decode('utf-8') + nouns.ix[noun].tha.decode('utf-8')
            d[num + dem + noun] = preNonPhrase
            postIsoPhrase = nouns.ix[noun].tha.decode('utf-8') + nums.ix[num].tha.decode('utf-8') + dems.ix[dem].tha.decode('utf-8')
            d[noun + num + dem] = postIsoPhrase
            postNonPhrase = nouns.ix[noun].tha.decode('utf-8') + dems.ix[dem].tha.decode('utf-8') + nums.ix[num].tha.decode('utf-8')
            d[noun + dem + num] = postNonPhrase

# num-adj
for num in nums.index:
    for adj in adjs.index:
        for noun in nouns.index:
            preIsoPhrase = nums.ix[num].tha.decode('utf-8') + adjs.ix[adj].tha.decode('utf-8') + nouns.ix[noun].tha.decode('utf-8')
            d[num + adj + noun] = preIsoPhrase
            preNonPhrase = adjs.ix[adj].tha.decode('utf-8') + nums.ix[num].tha.decode('utf-8') + nouns.ix[noun].tha.decode('utf-8')
            d[adj + num + noun] = preNonPhrase
            postIsoPhrase = nouns.ix[noun].tha.decode('utf-8') + adjs.ix[adj].tha.decode('utf-8') + nums.ix[num].tha.decode('utf-8')
            d[noun + adj + num] = postIsoPhrase
            postNonPhrase = nouns.ix[noun].tha.decode('utf-8') + nums.ix[num].tha.decode('utf-8') + adjs.ix[adj].tha.decode('utf-8')
            d[noun + num + adj] = postNonPhrase


            
    
# for phrase in d.keys():
#     createImage(phrase, d[phrase], buttonWidth/dpi, buttonHeight/dpi)

# createImage('-----', '-----', buttonWidth/dpi, buttonHeight/dpi)

# introText = u"ในการทดลองนี้ท่านจะได้เรียนภาษาใหม่โดยภาษาดังกล่าวจะมีลักษณะคล้ายกับภาษาไทยแต่ท่านจะพบลักษณะต่างบางประการ\nท่านจะต้องแปลวลีในภาษาไทยเป็นภาษาใหม่\nกด spacebar เพื่อดำเนินการต่อ"
            
trialTexts30 = {i: u'...เลือกตัวเลือกที่สอดคล้องกับสิ่งที่ท่านได้ยิน... ({}/30)'.format(i+1) for i in range 30}

createImage('intro', introText, 1200, 600)




