# -*- coding: utf-8 -*-


##### Modules #####
import matplotlib as mpl
mpl.use('pgf')
import seaborn as sns


import matplotlib.pylab as plt
from matplotlib.ticker import FuncFormatter
from matplotlib import ticker
from numpy import *
import scipy.stats as ss
import pandas as pd
#####


##### LaTeX Preamble #####
pgf_with_custom_preamble = {
	"font.family": "sans",
	"text.usetex": True,
	"pgf.rcfonts": False,
	"pgf.preamble": [
		r"\usepackage[MnSymbol]{mathspec}",
		r"\setsansfont[Mapping=tex-text, Numbers={Lowercase, Proportional}, Scale=1.5]{Linux Biolinum O}",
		r"\setmathfont(Digits,Greek,Latin)[Numbers={Lowercase, Proportional}, Scale=2]{Linux Biolinum O}"
		
	]
}
mpl.rcParams.update(pgf_with_custom_preamble)
#####



##### DATA #####
df = pd.read_csv('./U20Spanish_TestData.csv')

aggregators = {
     'binaryCorrect': mean,
}

gp = df.groupby(['ID', 'condition'], as_index=False).agg(aggregators)
gp.condition.replace('condition_AdjDem', 'Adj-Dem', inplace=True)
gp.condition.replace('condition_NumDem', 'Num-Dem', inplace=True)
gp.condition.replace('condition_AdjNum', 'Adj-Num', inplace=True)
#####




##### PLOTTING #####
f = plt.figure()
f.set_size_inches(5,3)


sns.set_style('white')
c = sns.color_palette('Set2', 4)
c.insert(0, c.pop(3))

order = ['Adj-Dem', 'Num-Dem', 'Adj-Num']

ax = plt.subplot()


sns.boxplot(
     data=gp,
     x='condition',
     order=order,
     y='binaryCorrect',
     # hue='bloc',
     ax=ax,
     # palette=c,
     color='white',
     width=0.5,
     # showfliers=False
     # saturation=0.8
)

sns.swarmplot(
     data=gp,
     x='condition',
     order=order,
     y='binaryCorrect',
     # hue='cons',
     ax=ax,
     # palette=c,
     alpha=0.75,
     color="black"
)

ax.plot(range(-1,4), [0.5]*5, color='grey', linestyle='--', linewidth=0.5)


def percfunc(x, pos=0): 
     return '%1.0f'%(100*x)
     
ax.set(ylim=(-0.1,1.1))
ax.yaxis.set_major_formatter(FuncFormatter(percfunc))

sns.despine(left=True, bottom=True)
lab = '''Scope-isomorphic
choice (%)'''
ax.set_ylabel(lab)
ax.set_xlabel('')
ax.set_title('Spanish')



plt.savefig("acc-box-dots.pdf", format='pdf', transparent=True, bbox_inches="tight")

