#!/usr/bin/env python
# encoding: utf-8


## reshape from "varA1 varB1 val11" 
## to crosstable varA1 varA2 varA3 ...
## 			varB1 val11 ...
## 			varB2 val21 ...

from sys import stdin
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f', dest='fill', default="NA", help='fill empty space with this default value')
parser.add_argument('-d', dest='delim', default=None, help='split by this delimiter')
parser.add_argument('-s', dest='sortKey', default=True, help='output sorted key')
args = parser.parse_args()

delim = args.delim
fill = args.fill
sortKey = args.sortKey
if sortKey != True:
	if sortKey.lower() in ["false", "f", "no", "0", ""]:
		sortKey = False

D = {}
varAs, varBs = set(), set()
# save
for line in stdin.readlines():
	if delim:
		ls = line.strip().split(delim)
	else:
		ls = line.strip().split()
	varA, varB, val = ls[0], ls[1], ls[2]
	D[(varA, varB)] = val
	varAs.add(varA)
	varBs.add(varB)
if sortKey:
	varAs = sorted(varAs)
	varBs = sorted(varBs)

# load
header = "\t" + "\t".join(list(varBs))
print(header)
for varA in varAs:
	line = varA + "\t" + "\t".join([D.get((varA, varB), fill) for varB in varBs])
	print(line)
		

