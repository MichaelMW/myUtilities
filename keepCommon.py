#!/bin/env python

from glob import glob
from sys import argv

kw=argv[1]
entryIdx=0  # build common entry based on which column

# indexing common entry
for ith, inFile in enumerate(glob(kw)):
	print "building common entry from {}...".format(inFile)
	with open(inFile) as f:
		if ith==0:
			commonEntry=[l.split()[entryIdx] for l in f.readlines()]
		else:
			entry=[l.split()[entryIdx] for l in f.readlines() if l.split()[entryIdx] in commonEntry]
			commonEntry=entry
	
# loop back to each files. 
for inFile in glob(kw):
	print "retrieving common entry from {}...".format(inFile)
	with open(inFile) as f:
		towriteList=[l.strip() for l in f.readlines() if l.split()[entryIdx] in commonEntry]
	outFile=inFile+".common"
	with open(outFile, 'w') as f:
		f.write('\n'.join(towriteList))
	print "Written to {}!".format(outFile)
	
