#!/bin/env python

import re
import os
import argparse
import sys 
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

## input kmer, output a meme file

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inTsv", help="input eg. of kmer.tsv: ATTCGGA\nTGGCACGG" or "kmer1\tATTCGGA\nkmer2\tTGGCACGG if ID is specified")
parser.add_argument("-p", "--psuedoCount", help="psuedoCount default=0.1, kmer has 0.9, rest total=0.1", default=0.1)
args = parser.parse_args()

def main():
		
	# checking args
	pc = float(args.psuedoCount)

	# start running
	towriteList = []
	header = """
MEME version 4.5

ALPHABET= ACGT

strands: + 

Background letter frequencies (from
A 0.295 C 0.205 G 0.205 T 0.295

"""

	# check overlap
	IDs = []
	kmers = []
	for line in sys.stdin.readlines():
		if len(line.split())==2:
			ID, kmer = line.split()[:2]	
		else:
			kmer = line.strip()
			ID = kmer
		if ID in IDs:
			print "## {} already existed, skipping this".format(ID)
			continue
		else:
			IDs.append(ID)
		if kmer in kmers:
			print "## warning: duplicated kmers: {}".format(kmer)
		else:
			kmers.append(kmer)
		memeInfo = "MOTIF {}\nletter-probability matrix: alength= 4 w= {} nsites= 100 E= 1.0e-1\n{}".format(ID, len(kmer), kmer2tab(kmer,pc))
		towriteList.append(memeInfo)
	
	# output 
	print header
	print "\n\n".join(towriteList)

pass

def kmer2tab(kmer, pc):
	D = {nt:i for i, nt in enumerate("ACGT")}
	tab = [ [1-pc if i==D[mer] else pc/3 for i in range(4)] for mer in kmer]
	return "\n".join([" "+'\t'.join(map(str, line)) for line in tab])

if __name__=='__main__':
	main()
