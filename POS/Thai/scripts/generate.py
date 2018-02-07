import os
from itertools import product
from collections import defaultdict
from subprocess import call, STDOUT, DEVNULL

FONT = 'Helvetica'
FONTSIZE = 48
INKSCAPE_PATH = '/opt/local/bin/inkscape'

template = '''<svg width='400px' height='80px' xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' xmlns:svg='http://www.w3.org/2000/svg' xmlns='http://www.w3.org/2000/svg' version='1.1'>
	<text x='200px' y='40px' style='font-family:"{font}"; font-size:{fontsize}px; text-anchor:middle;'>{label}</text>
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

def load_words(csv_file):
	words_by_category = defaultdict(list)
	with open(csv_file, encoding='utf-8') as file:
		for i, line in enumerate(file):
			if i == 0:
				continue
			eng, thai, trans, category = line.strip().split(',')
			words_by_category[category].append((eng, thai))
			if category in ['adj', 'dem', 'num']:
				words_by_category['mod'].append((eng, thai))
	return words_by_category

def iter_words_orders(words_by_category, word_order):
	word_sets = [words_by_category[category] for category in word_order]
	for label_combination in product(*word_sets):
		english_words = [word_pair[0] for word_pair in label_combination]
		thai_words = [word_pair[1] for word_pair in label_combination]
		yield english_words, thai_words

def make_images_in_whatever_fucking_word_orders_you_want(csv_file, out_dir, word_orders):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    words_by_category = load_words(csv_file)
    for word_order in word_orders:
        for english_words, thai_words in iter_words_orders(words_by_category, word_order):
            fileName = out_dir+''.join(english_words)+'.png'
            # print(fileName)
            if not os.path.isfile(fileName):
                make_image(out_dir, english_words, thai_words)


wordOrders = [
    ('mod','noun'),
    ('noun','mod'),
    ('dem','adj','noun'),
    ('adj','dem','noun'),
    ('dem','num','noun'),
    ('num','dem','noun'),
    ('num','adj','noun'),
    ('adj','num','noun'),
    ('noun','adj','num'),
    ('noun','num','adj'),
    ('noun','dem','num'),
    ('noun','num','dem'),
    ('noun','dem','adj'),
    ('noun','adj','dem')
]

wordOrders = [
    ('noun','mod'),
    ('noun','adj','dem'),
    ('noun','adj','num'),
    ('noun','num','dem')
]
    

    
make_images_in_whatever_fucking_word_orders_you_want('../stimuli/tha/vocab.csv', out_dir='../stimuli/tha/images/BIG', word_orders=wordOrders)

