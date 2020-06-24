#!/usr/bin/env python
from __future__ import division
from sys import stdin
from signal import signal, SIGPIPE, SIG_DFL
from scipy.stats import chi2_contingency
import argparse

# chi square test with yates correction
# with pseudo count = e
# H0: E1/E2 <= O1/O2

# input columns are E1, E2, O1, O2, respectively

# todo: notice how having multiple 0s will cause problem
# eg. 
# echo -e "1 0 1 0" | chiSquare.1t.py
# 0.5
# echo -e "1 0 2 0" | chiSquare.1t.py
# 1.0
# echo -e "1 0 0 0" | chiSquare.1t.py
# error

signal(SIGPIPE,SIG_DFL)

# parsing args
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--tail", default=1,
	help = "1 tail or 2 tails test. default is one tail, with H0:E1/E2 <= O1/O2")
parser.add_argument("-p", "--pseudocount", default=0,
	help = "pseudocount, larger pseudocount leads to lower FDR")
parser.add_argument("-c", "--correction", default=0,
	help = "chi square test yates correction, use 1 for True or 0 for False")
parser.add_argument("-r", "--pcr", default=0.1,
	help = "pseudocount ratio, which is used to multiply colmean of E1, E2 and add to E1&O1, E2&O2; takes longer time, more assumption that leads to group bias. But can be more accurate; use larger pcr leads to lower FDR")
parser.add_argument("-d", "--direction", default=1,
	help = "direction of 1 tail comparison. default =1: E1/E2 <= O1/O2; use other for E1/E2 >= O1/O2")
args = parser.parse_args()
pc = float(args.pseudocount)
if args.pcr:
	pcr = float(args.pcr)
else:
	pcr = False
tail = int(args.tail)
direction = int(args.direction)
yates = bool(int(args.correction))

# read data
ls = stdin.readlines()

# use average for pseudocount ratio, count colmeans of E1, E2, O1, O2. 
# though only use E1 E2. 
if pcr != 0:
	colmeans = [sum(map(float, col))/len(col) for col in zip(*[l.strip().split() for l in ls])]

# main
for l in ls:
	if pcr:
		# notice the mod here. Add E1 E2 to (E1 and O1), (E2 and O2). 
		e1, e2, o1, o2 = [float(i) + pcr * colmeans[idx%2] for idx, i in enumerate(l.strip().split())]
	else:
		e1, e2, o1, o2 = [float(i) + pc for i in l.strip().split()]
	
	#print e1, e2, o1, o2
	try:
		g, p, dof, expctd = chi2_contingency([[e1, e2], [o1, o2]], correction = yates)
	except:
		print("errorline: \n{} \b{}, {}, {}, {}".format(l, e1, e2, o1, o2))
		exit()
	if tail == 1:
		if direction == 1:
			if e1 / e2 <= o1 / o2:
				print(1- p/2)
			else:
				print(p/2)
		else:
			if e1 / e2 >= o1 / o2:
				print(1- p/2)
			else:
				print(p/2)
			
	else:
		print(p)


