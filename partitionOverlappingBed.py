#!/usr/bin/env python
# encoding: utf-8

## input a bedfile with overlapping regions
## output a bedfile with continous regions divided by incremental boundaries from input
## emulates bedops --partition, but fix a few bugs from that. 

from collections import defaultdict
from sys import stdin, argv
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)


## check input is number
def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False



def chain_set_to_list(positions, chrm):
	position_list = sorted(list(set(positions)))
	to_append = [f"{chrm}\t{position_list[i]}\t{position_list[i+1]}" for i in range(len(position_list) - 1)]
	return to_append

def partition_overlapping_regions(regions, chrm):
	results = []
	position_list = []
	sorted_regions = sorted(regions)
	cache_start, cache_end = sorted_regions[0]
	position_list += [cache_start, cache_end]

	# loop through regions, check if it's in a contig. 
	for region in sorted_regions[1:]:
		start, end = region
		assert start <= end
		# when current region is within a contig, store position in the list
		if start <= cache_end:
			position_list += [start, end]
			cache_end = max(cache_end, end)
		# when current region is gapped. 
		else:
			# dump positions into results
			results += chain_set_to_list(position_list, chrm)
			# reset new postion
			position_list = [start, end]
			cached_start, cache_end = start, end
	# final dump:
	results += chain_set_to_list(position_list, chrm)
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
	results = partition_overlapping_regions(regions, chrm)
	for result in results:
		print(result)
