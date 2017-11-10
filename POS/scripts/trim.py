# -*- coding: utf-8 -*-

import os
import re

# chemin = os.getcwd()
chemin = "../stimuli/"
os.chdir(chemin)
files = os.listdir('.')
p = re.compile('.*\.wav')

for fname in files:
    m = p.match(fname)
    if m:
        word = fname.split('.')[0]
        newFile = word + "-begtrim.wav"
        command = "sox {} {} trim 0.5".format(fname, newFile)
        os.system(command)
        newnewFile = word + "-trim.wav"
        command = "sox {} {} trim 0 -0.5".format(newFile, newnewFile)
        os.system(command)
    else:
        continue
            
