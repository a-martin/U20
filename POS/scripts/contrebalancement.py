# -*- coding: utf-8 -*-

import re
import pandas as pd

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