#!/usr/bin/env python

## input a file, output a column split file of the combination. 
## eg. input inFile
# A
# B
# C
## output 
# A B
# A C
# B C


from sys import stdin
from itertools import combinations


combineFactor=2
List=[]
for line in stdin.readlines():
	List.append(line.strip())

for i in combinations(List,2):
	print "\t".join(i)

