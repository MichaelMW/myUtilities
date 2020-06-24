#!/usr/bin/env python
# encoding: utf-8


## input a sequence and the windows size. eg. "ATCGAGACG...120". any white space will to. 
## eg. echo "ATCGAGACG" | ./faa2gc.py 120
## output GC content sliding window, eg. 0.5, 0.51, 0.49 ...

from sys import stdin, argv

fa = stdin.readline().strip()
try:
	win = int(argv[1])
except IndexError:
	win = 1

## get GC
def fa2cg(fa, win, step=1):
	cg_rates = []
	fa = fa.upper()
	faLen = len(fa)
	subfa = fa[:win]

	cg = sum([1 for nt in subfa if nt in "CG"])
	cg_rate = round(cg*1.0/win, 3)
	cg_rates.append(cg_rate)

	for i in range(1,faLen-win+1,step):
		nt_out = fa[i-1]
		nt_in = fa[i+win-1]
		if nt_in in "CG":
			cg += 1
		if nt_out in "CG":
			cg -= 1
		cg_rate = round(cg*1.0/win, 3)
		cg_rates.append(cg_rate)

	return(cg_rates)
	
## sliding windows
print(" ".join(map(str,fa2cg(fa, win))))

