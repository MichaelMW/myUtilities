#!/bin/env python
import re
from sys import stdin, stderr, argv
from signal import signal, SIGPIPE, SIG_DFL
import argparse

signal(SIGPIPE,SIG_DFL)




## input meme file, output kmers.tsv to pipe 
## parse args
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inMeme", help="Input meme file")
parser.add_argument("-a", "--AUC_cutoff", help="Input AUC cutoff.")
parser.add_argument("-p", "--pval_cutoff", help="Input fisher pval cutoff.")
args = parser.parse_args()


## check args
if args.inMeme:
	inMeme=args.inMeme
	with open(inMeme) as f:
		inData = f.read()
else:
	inData=stdin.read()
if args.AUC_cutoff:
	AUC_cutoff=float(args.AUC_cutoff)
else:
	AUC_cutoff=-1
if args.pval_cutoff:
	pval_cutoff=float(args.pval_cutoff)
else:
	pval_cutoff=1

## initialize
header = inData.split("MOTIF")[0]
NTs = "ACGT"

print header
for motifInfo in inData.split("MOTIF")[1:]:
	motifID = motifInfo.split('\n')[0].strip()	
	AUC = float(motifID.split("_")[2])
	pval = float(motifID.split("_")[3])
	if AUC>=AUC_cutoff and pval<=pval_cutoff:
		print "MOTIF "+motifInfo.strip()+"\n"

	#motifKmer = [ max((float(rate),i) for line in motifInfo.split('\n')[2:] for i, rate in enumerate(line.split())) ]
	#print "{}\t{}".format(motifID,"".join(motifKmer))
	#print motifKmer


