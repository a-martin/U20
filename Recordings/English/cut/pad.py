# -*- coding: utf-8 -*-

import os
import re

# chemin = os.getcwd()
chemin = "./modifiers/"
os.chdir(chemin)
files = os.listdir('.')
p = re.compile('.*-am\.wav')

dico = {}

for fname in files:
    m = p.match(fname)
    if m:
        word = fname.split('-')[0]
        newfile = word + "-pad.wav"
        command = "sox {} {} pad 0.5 0.5".format(fname, newfile)
        os.system(command)
    else:
        continue
            
