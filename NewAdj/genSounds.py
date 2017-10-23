import pandas as pd
from pandas import *
import numpy as np
import os # for writing files
from os import walk # for getting list of filenames in a directory
from os import listdir
import subprocess # for running shell script

# First, set your path, e.g.
#os.chdir('/Users/jenny/Sites/U20NewAdj')
os.chdir('/Users/jenny/DropBox/U20NewAdjExperiment/U20NewAdj')

# You can use a file with a single column, or with multiple columns
# Multiple columns:
df = pd.read_csv('all_vocab.csv')
nouns = df[(df.cat == 'noun')]
nums = df[(df.cat == 'num')]
nums = nums.reset_index(drop=True)
adjs = df.loc[(df.cat == 'adj_inner') | (df.cat == 'adj_outer') | (df.cat == 'adj_original')]
adjs = adjs.reset_index(drop=True)

# set a path to save the files in
mypath='sounds/'
        	
# or to make combinations of words   	
for n in range(0,nouns.word.count()):
    noun = nouns.word[n].split('_')[0]
    for a in range(0,adjs.word.count()): 
        sound_i = ['say', '-v','Alex','[[emph+]]',noun,'[[slnc 50]]','[[emph +]]',adjs.word[a],'-o',mypath+noun+adjs.word[a]+'.wv']
        subprocess.call(sound_i)

# or to make combinations of words   	
for n in range(0,nouns.word.count()):
    for m in range(0,nums.word.count()):
        if nums.word[m] == 'one': noun = nouns.word[n].split('_')[0]
        else: noun = nouns.word[n].split('_')[1]
        sound_i = ['say', '-v','Alex','[[emph+]]',noun,'[[slnc 50]]','[[emph +]]',nums.word[m],'-o',mypath+noun+nums.word[m]+'.wv']
        subprocess.call(sound_i)


# Note that the say command outputs files in wav format, but with the file extension .wv (who knows why...!)
# First rename all the .wv files as .wav
# Then from there you can convert them to other formats as needed e.g., ogg, and mp3, can use sox or ffmpeg (may need to install these)
f = []
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    break

for i in range(1,len(f)):
    filename=f[i].split(".")[0]
    sound_i = ['/Applications/sox-14.4.1/sox', mypath+filename+'.wv', mypath+filename+'.wav']
    subprocess.call(sound_i)
    #ogg
    sound_i = ['/Applications/sox-14.4.1/sox', mypath+filename+'.wav', mypath+filename+'.ogg']
    subprocess.call(sound_i)
    #mp3
    sound_i = ['ffmpeg','-i',mypath+filename+'.wav','-codec:a','libmp3lame',mypath+filename+'.mp3']    
    subprocess.call(sound_i)

# Get rid of those useless .wv files :)
test=os.listdir(mypath)
for item in test:
    if item.endswith(".wv"):
        os.remove(os.path.join(mypath, item))