#!/usr/bin/env python
# encoding: utf-8


### set operation between file A and B, on column 1. 

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-a', dest='inA', help='File A')
parser.add_argument('-b', dest='inB', help='File B')
parser.add_argument('-o', dest='operation', default = "u", help='"|/u" for A|B union (Default), "&/i" for A&B intersect, "-/d" for A-B difference')

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

### parse and check args. 
args = parser.parse_args()
inA = args.inA
inB = args.inB
operation = args.operation.lower()

### read file lines to a set
def file2set(inFile):
	returnSet = set()
	with open(inFile) as f:
		for l in f.readlines():
			returnSet.add(l.strip())
	return returnSet

setA = file2set(inA)
setB = file2set(inB)

### operation
if operation in ["u", "|"]:
	setResult = setA | setB
elif operation in ["i", "&"]:
	setResult = setA & setB
elif operation in ["d", "-"]:
	setResult = setA - setB

for line in setResult:
	print(line)
