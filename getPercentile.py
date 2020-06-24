#!/usr/bin/env python
from __future__ import division
from signal import signal, SIGPIPE, SIG_DFL
from sys import stdin
import argparse


signal(SIGPIPE,SIG_DFL)


parser = argparse.ArgumentParser()
parser.add_argument("-b", "--bin", default=10,
	help="bin: number of bins")
parser.add_argument("-s", "--sorted", action='store_true',
	help="if input list is sorted")
args = parser.parse_args()


global bin
bin = int(args.bin)
inputIsSorted = args.sorted

def printPerc(List):
	for i in range(bin):
		index = int(len(List) * i / bin)
		value = List[index]
		percentile = int(100 * i / bin)
		print "{}%\t{}".format(percentile, value)
	print "100%\t{}".format(List[-1])


List = [float(line.strip()) for line in stdin.readlines() if line.strip()]

if inputIsSorted:
	printPerc(List)
else:
	sortedList = sorted(List)
	printPerc(sortedList)

