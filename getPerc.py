#!/usr/bin/env python
from __future__ import division
from scipy.stats import rankdata
from signal import signal, SIGPIPE, SIG_DFL
from sys import stdin
import argparse


signal(SIGPIPE,SIG_DFL)


def num2perc(L):
	d=2
	perc = rankdata(L, "average")/len(L)
	perc_re2 = map(lambda x: '{number:0.{digit}f}%'.format(number=x*100,digit=d), perc)  # use % format
	return perc_re2

def num2percSci(L):
	perc = rankdata(L, "average")/len(L)
	perc_re2 = map(lambda x: "%.2E"%x, perc)  # use sci format
	return perc_re2

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--percentageFormat", action="store_true")
args = parser.parse_args()


List = [float(line.strip()) for line in stdin.readlines() if line.strip()]

if args.percentageFormat:
	print("\n".join(map(str,num2perc(List))))
else:
	print("\n".join(map(str,num2percSci(List))))
	
