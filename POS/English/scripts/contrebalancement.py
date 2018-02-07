# -*- coding: utf-8 -*-

import re
import pandas as pd
import random



##

def drawSet(ID, df):
    if ID != 'dem':
        train = pd.concat([df.sample(5)] * 3)
        test = df.copy()
    elif ID == 'dem':
        # repeat four times and drop one line
        train = pd.concat([df] * 4)[:15]
        # repeat three times and drop two lines
        test = pd.concat([df] * 3)[:10]

    return {'train': train, 'test': test}

##


lex = pd.read_csv('../stimuli/vocab.csv')

noms = pd.read_csv('../stimuli/nouns.csv')
adjs = lex[lex.cat=='adj']
nums = lex[lex.cat=='num']

# sample 20 nouns..half will be repeated, thus 30 trials
noms = noms.sample(20)
repeatNoms = noms.sample(10)
noms = pd.concat([noms, repeatNoms])

mods = pd.read_csv('../stimuli/modifiers.csv')


innerID, outerID = cond.split('-')
IDs = [innerID, outerID]

inOutSets = {ID:mods[mods.cat==ID].sample(frac=1).reset_index(drop=True) for ID in IDs}



inner, outer = [drawSet(ID, inOutSets[ID]) for ID in IDs]
        





# sample 5 adjs or nums to repeat 3 times, thus 15 trials
condition = True
if condition:
    adjs = mods[mods.cat=='adj'].sample(5)
    adjs = pd.concat([adjs, adjs, adjs])
else:
    nums = mods[mods.cat=='num'].sample(5)
    nums = pd.concat([nums, nums, nums])














































abx = pd.read_csv('stim_list.csv', sep=';')

# v = ['re', 'ru']
# sh = 'sh'
contrastes = [('b', 'p'), ('k', 'g')]
clabels = ['native', 'emerging']

trials = []

def makefour(A, B):
    four = [
        [A, B, A, 'A'],
        [A, B, B, 'B'],
        [B, A, A, 'B'],
        [B, A, B, 'A']
    ]
    return four


for f in abx.frame.unique():
    for n,cont in enumerate(contrastes):
        A = abx[abx.frame==f][abx.phon==cont[0]].iloc[0]['item']
        B = abx[abx.frame==f][abx.phon==cont[1]].iloc[0]['item']
        t1 = makefour(A,B)

        # [
        #     [A+'_'+v[0], B+'_'+v[1], A+'_'+sh, 'A', cont[0]], # eg b-re p-ru b-sh
        #     [A+'_'+v[1], B+'_'+v[0], A+'_'+sh, 'A', cont[0]], # eg b-ru p-re b-sh
        #     [A+'_'+v[0], B+'_'+v[1], B+'_'+sh, 'B', cont[1]], # eg b-re p-ru p-sh
        #     [A+'_'+v[1], B+'_'+v[0], B+'_'+sh, 'B', cont[1]], # eg b-ru p-re p-sh
        # ]

        # A = abx[abx.frame==f][abx.phon==cont[1]].iloc[0]['item']
        # B = abx[abx.frame==f][abx.phon==cont[0]].iloc[0]['item']
        # t2 = makefour(A,B)

        # [
        #     [A+'_'+v[0], B+'_'+v[1], A+'_'+sh, 'A', cont[1]], # eg p-re b-ru p-sh
        #     [A+'_'+v[1], B+'_'+v[0], A+'_'+sh, 'A', cont[1]], # eg p-ru b-re p-sh
        #     [A+'_'+v[0], B+'_'+v[1], B+'_'+sh, 'B', cont[0]], # eg p-re b-ru b-sh
        #     [A+'_'+v[1], B+'_'+v[0], B+'_'+sh, 'B', cont[0]], # eg p-ru b-re b-sh
        # ]


        for t in (t1):
            trials.append(t+[clabels[n]]+[f]+['test'])

trials = pd.DataFrame(trials)

header = [
    'A',
    'B',
    'X',
    'bonne_rep',
    # 'cible',
    'contraste',
    'frame',
    'bloc'
]

trials.columns = header

trials.to_csv('trials.csv', index=None)            