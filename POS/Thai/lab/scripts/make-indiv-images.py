import os
from itertools import product
from collections import defaultdict
from subprocess import call, STDOUT, DEVNULL

FONT = 'Helvetica'
FONTSIZE = 18
INKSCAPE_PATH = '/opt/local/bin/inkscape'

template = '''<svg width='800px' height='800px' xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' xmlns:svg='http://www.w3.org/2000/svg' xmlns='http://www.w3.org/2000/svg' version='1.1'>
	<text x='20' y='400px' style='font-family:"{font}"; font-size:{fontsize}px; text-anchor:left;'>{label}</text>
</svg>'''

def make_image(out_dir, english_words, thai_words):
	filename = ''.join(english_words)
	filepath = os.path.join(out_dir, filename)
	thai_string = ''.join(thai_words)
	svg = template.format(label=thai_string, font=FONT, fontsize=FONTSIZE)
	with open(filepath + '.svg', mode='w', encoding='utf-8') as file:
		file.write(svg)
	call([INKSCAPE_PATH, filepath + '.svg', '-e', filepath + '.png'], stdout=DEVNULL, stderr=STDOUT)
	call(['rm', filepath + '.svg'])


chemin = '../stimuli/tha/consignes/'  

# make_image(chemin, 'traduisez', u'วลีที่ต้องแปล')

# for i in range(50):
#     make_image(chemin, '50trial{}'.format(i+1), u'...เลือกตัวเลือกที่ผู้พูดของภาษาใหม่จะพูด...({}/50)'.format(i+1))

intro = u'''
ในการทดลองนี้ ท่านจะได้เรียนภาษาใหม่ โดยภาษาดังกล่าวจะมีลักษณะคล้ายกับภาษาไทย แต่ท่านจะพบลักษณะต่างบางประการ
\n\n
ท่านจะต้องแปลวลีในภาษาไทยเป็นภาษาใหม่
'''

make_image(chemin, 'intro', intro)




