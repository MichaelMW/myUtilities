#!/usr/bin/env python
from sys import stdin
from signal import signal, SIGPIPE, SIG_DFL
from scipy.stats import pearsonr


signal(SIGPIPE,SIG_DFL)

X, Y = [], []
for line in stdin.readlines():
	ls = line.strip().split()
	X.append(float(ls[0]))
	Y.append(float(ls[1]))

print pearsonr(X, Y)
