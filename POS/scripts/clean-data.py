# -*- coding: utf-8 -*-

import pandas as pd
import os, re
from numpy import nan

chemin = "../data/test/"
os.chdir(chemin)
files = os.listdir('.')
p = re.compile('.*\.csv')

cols = [
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
df = pd.DataFrame(columns=cols)

for fname in files:
    m = p.match(fname)
    if m:
        df = df.append(pd.read_csv(fname), ignore_index=True)
    else:
        continue


vocab = pd.read_csv('../../stimuli/vocab.csv')
nouns = vocab[vocab.cat=='noun'].copy()
nounList = list(vocab.sing) + list(vocab.plur)

mods = pd.read_csv('../../stimuli/modifiers.csv')
nums = mods[mods.cat=='num']
dems = mods[mods.cat=='dem']
adjs = mods[mods.cat=='adj']
        
def isPost(i):

    row = df.ix[i]

    if row.nbMods == 2:
        return nan

    response = row.response.split(' ')
    if response[0] in nounList:
        return 1
    else:
        return 0


def checkResp(outer, inner, response):
    if response[1] in list(inner.word) and response[2] in list(outer.word):
        return 1
    else:
        return 0

                
def isIso(i):

    row = df.ix[i]

    if row.nbMods == 1:
        return nan

    cond = row.cond
    response = row.response.split(' ')
    
    # check that noun is first
    if response[0] not in nounList:
        return 0

    if cond == 'dem-adj':
        outer = dems
        inner = adjs

    elif cond == 'dem-num':
        outer = dems
        inner = nums

    elif cond == 'num-adj':
        outer = nums
        inner = adjs

    return checkResp(outer, inner, response)
        
            

df['nbMods'] = df.modInner.map(lambda x: 2 if x is not nan else 1)
df['iso'] = df.index.map(lambda x: isIso(x))
    
df.to_csv(chemin+'ENGtest.csv', index=False)


