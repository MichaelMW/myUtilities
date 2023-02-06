#!/usr/bin/env python
# encoding: utf-8

# input a such bed file with many non-overlapping regions. But some regions are next to each other with 0 or 1 bp distance. 
# eg. 
# chr1 1 2
# chr1 2 30
# chr1 50 200
# chr1 201 300
# chr1 1000 2000
#  
# I want to merge the smaller regions with <= X bp distance when possible, so that each regions have >= Y bp in length. let's say X=1, Y=100
# 
# ie. output
# chr1 1 30
# chr1 50 200   #### already 150 in length > 100, no need to merge
# chr1 201 300
# chr1 1000 2000




from collections import defaultdict
from sys import stdin, argv
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

X=1
Y=100

## check input is number
def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def merge_regions(regions, chrm, X, Y):
	results = []
	sorted_regions = sorted(regions)
	start, end = sorted_regions[0]
	position_list = [start, end]

	for region in sorted_regions[1:]:
		start, end = region
		if start <= position_list[1] + X and end - start < Y: ## greedy
			position_list[1] = max(end, position_list[1])
		else:
			results.append(f'{chrm}\t{position_list[0]}\t{position_list[1]}')
			position_list = [start, end]
	results.append(f'{chrm}\t{position_list[0]}\t{position_list[1]}')
	return results


####### main
## input from argv[1]
try:
	inFile = argv[1]
	with open(inFile) as f:
		data = f.readlines()
## input from stdin
except IndexError:
	data = stdin.readlines()

## read input lines. 
chrm2regions = defaultdict(list)
for line in data:
	ls = line.strip().split()
	chrm, start, end = ls[:3]
	assert is_number(start) and is_number(end) and int(start) <= int(end)
	chrm2regions[chrm].append([int(start),int(end)])

## output lines:
for chrm in sorted(chrm2regions.keys()):
	regions = chrm2regions[chrm]
	results = merge_regions(regions, chrm, X, Y)
	for result in results:
		print(result)
