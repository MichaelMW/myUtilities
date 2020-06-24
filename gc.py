#!/usr/bin/env python
# encoding: utf-8

from sys import stdin

for line in stdin.readlines():
	line = line.strip().upper()
	cg, n  = 0, 0
	for c in line:
		n+=1
		if c in "CG":
			cg+=1
	cg_rate = round(cg*1.0/n,3)
	print(cg_rate)
