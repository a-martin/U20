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
        
def isPost(i):

    row = df.ix[i]

    if row.nbMods == 2:
        return nan

    response = row.response.split(' ')
    if response[0] in nounList:
        return 1
    else:
        return 0
    
def isIso(i):

    row = df.ix[i]

    if row.nbMods == 1:
        return nan

    cond = row.cond

    




    iso = 0
       
    return iso

df['nbMods'] = df.modInner.map(lambda x: 2 if x is not nan else 1)
df['iso'] = df.index.map(lambda x: isIso(x))
    
df.to_csv(chemin+'ENGtest.csv', index=False)



