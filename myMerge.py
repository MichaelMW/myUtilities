#!/usr/bin/env python
# encoding: utf-8

## README
#merge the values of two files based on common keys. 
#keys are given by column entries from the two files using -e1 and -e2. 
#	e1 for the first file, eg. -e1 1,2 mean the keys are given by column 1 and 2 from file 1. 
#	e2 for the second file. 
#values are given by column entries from the two files using -c1 and -c2. 
#If common keys are not found, -f is used to provide a default filler. 

## usage example:
## myMerge -a gen.fas.CX_report.txt -b hg19_pe_f150r150_dir.ch3 -e1 1,2 -e2 1,2 -c1 4 -c2 5 -f 0

import argparse
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

parser = argparse.ArgumentParser()
parser.add_argument('-a', dest='inA', help='The first file.')
parser.add_argument('-b', dest='inB', help='The second file.')
parser.add_argument('-m', dest='mode', help='determine the key from (A), (B), (A-B), (B-A), (U)nion or (I)ntersect; default Union', default="U")
parser.add_argument('-e1', dest='e1', default="1", help='Key column entries from the first files. Starts with 1, separated by commas,  eg. 1,2,3. Default 1.')
parser.add_argument('-e2', dest='e2', default="1", help='Key column entries from the second files. Starts with 1, separated by commas, eg. 1,2,3. Default 1.')
parser.add_argument('-c1', dest='c1', default="2", help='Value column entries from the first files. Starts with 1, separated by commas, eg. 1,2,3. Default 2.')
parser.add_argument('-c2', dest='c2', default="2", help='Value column entries from the second files. Starts with 1, separated by commas, eg. 1,2,3. Default 2.')
parser.add_argument('-f', dest='filler', default="0", help='If common keys are not found, -f is used to provide a default filler. Tips: use $\'\\t\' for tabs. Default 0.')
args = parser.parse_args()

## split columns
def arg2cols(string):
	cols = [int(col) for col in string.split(",")]
	return cols

## args
inA = args.inA
inB = args.inB
mode = args.mode.lower()
e1 = arg2cols(args.e1)
e2 = arg2cols(args.e2)
c1 = arg2cols(args.c1)
c2 = arg2cols(args.c2)
filler = args.filler

## return dict with entry = e and key = c. 
def file2dict(inFile, e, c):
	d = {}
	with open(inFile) as f:
		for l in f.readlines():
			ls = l.strip().split()
			key = tuple([ls[ei-1] for ei in e])
			item = [ls[ci-1] for ci in c]
			d[key] = item
	return d
	
## list2print
def list2print(l):
	if isinstance(l, str):
		toPrint = l
	else:
		toPrint = "\t".join(str(i) for i in list(l))
	return toPrint

## merge
dA = file2dict(inA, e1, c1)
dB = file2dict(inB, e2, c2)
if mode == "a":
	keyMerged = sorted(set(dA.keys()))
elif mode == "b":
	keyMerged = sorted(set(dB.keys()))
elif mode == "i" or mode == "intersect":
	keyMerged = sorted(set(dA.keys()) & set(dB.keys()))
elif mode == "a-b":
	keyMerged = sorted(set(dA.keys()) - set(dB.keys()))
elif mode == "b-a":
	keyMerged = sorted(set(dB.keys()) - set(dA.keys()))
elif mode =="u" or mode =="union":
	keyMerged = sorted(set(dA.keys()) | set(dB.keys()))
else:
	print("Unrecognized mode={}".format(mode))
	exit
for keyM in keyMerged:
	itemA = dA.get(keyM, filler)
	itemB = dB.get(keyM, filler)
	print("{}\t{}\t{}".format(list2print(keyM), list2print(itemA), list2print(itemB)))
