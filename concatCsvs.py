#!/usr/bin/env python
# encoding: utf-8

### 
from sys import argv
import pandas as pd
from glob import glob


### eg. ./thisScript.py "*.results.csv" merged.csv
### input strings of files to be concat together. 
### output a merged file 
### merge based one common column names 
### column names not shared among files would be filled with empty spaces. 

### todo: support sep to other delimiter, 
### todo: support other filler. 

globStrings = argv[1]
outFile = argv[2]

dfm = pd.DataFrame()

for inFile in glob(globStrings):
	print(inFile)
	df = pd.read_table(inFile, sep=",")
	dfm = pd.concat([dfm, df], axis=0) if (not df.empty) else df

dfm.to_csv(outFile, index=False)

