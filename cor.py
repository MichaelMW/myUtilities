#!/usr/bin/env python
from sys import stdin, argv
from signal import signal, SIGPIPE, SIG_DFL
from scipy.stats import pearsonr, spearmanr

signal(SIGPIPE,SIG_DFL)

## spearman, eg. cat test.tsv| cor.py 2
## pearson, eg. cat test.tsv| cor.py [1]

try:
	mode=argv[1]
except:
	mode="1"

X, Y = [], []
for line in stdin.readlines():
	ls = line.strip().split()
	X.append(float(ls[0]))
	Y.append(float(ls[1]))

if mode=="2":
	co, pval = spearmanr(X,Y)
	print('{}\t{}'.format(co, pval))
else:
	co, pval = pearsonr(X,Y)
	print('{}\t{}'.format(co, pval))
