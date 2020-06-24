#!/usr/bin/env python
# encoding: utf-8


from scipy.stats import ttest_1samp
from sys import stdin, argv

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-m', dest='popmean', default="0", help='population mean')
parser.add_argument('-t', dest='tail', default="1", help='single tail, default to h1: input values > mean')
args = parser.parse_args()
popmean = float(args.popmean)
tail = float(args.tail)

## input 
vals = [float(l.strip()) for l in stdin.readlines()]
if len(vals)>1:
	t, pval = ttest_1samp(vals, popmean)

	if int(tail)==1:
		if t>0:
			pval = pval/2
		else:
			pval = 1- pval/2
else:
	pval="NA"

print(pval)



