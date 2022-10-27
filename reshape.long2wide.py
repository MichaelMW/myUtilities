#!/usr/bin/env python
# encoding: utf-8

## reshape from "varA1 varB1 val11"  [long format]

## to crosstable varA1 varA2 varA3 ... [wide format]
## 			varB1 val11 ...
## 			varB2 val21 ...

from sys import stdin
import pandas as pd
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

## define the default method of aggregating values, by listing them separated by ","
def myList(values):
	return ",".join(map(str, values))

## input args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-e', dest='entries', default=1, help='column name(s) to build entry key on, sep by ",", eg. "sampleID,runID" means matching the column named "sampleID"')
parser.add_argument('-c', dest='columns', default=2, help='column name(s) to build columns/groupers on, sep by ",", eg. "variantType"')
parser.add_argument('-v', dest='values', default=3, help='column name(s) to build values on, sep by ",", eg. "called"')
parser.add_argument('-a', dest='aggfunc', default=myList, help='function to aggregate values on. eg. "sum", default = list')
parser.add_argument('-f', dest='fill', default="NA", help='fill empty space with this default value, default = NA')
args = parser.parse_args()

def parseColumnName(string, df_columns):
	strings = str(string).split(",")
	try:
		float(strings[0])
	except ValueError:
		pass 
	else:
		# input is column index like 1,2,3
		if float(strings[0]).is_integer():
			try:
				strings = [df_columns[int(string)-1] for string in strings]
			except IndexError:
				print(f'check index strings is 1-indexed columns, and is not out of range. \nstrings:{strings}\ncolumns:"{df_columns}"')
	return strings

df_long = pd.read_table(stdin)
df_columns = df_long.columns

index 	= parseColumnName(args.entries, df_columns)
columns = parseColumnName(args.columns, df_columns)
values 	= parseColumnName(args.values, df_columns)
aggfunc = args.aggfunc
fill 	= args.fill

df_wide = pd.pivot_table(df_long, index = index, columns = columns, values = values, aggfunc = aggfunc, fill_value = fill)
df_wide = df_wide.reset_index()
df_wide.columns = ['_'.join(filter(None,col)).strip() for col in df_wide.columns.values]
df_wide = df_wide.to_csv(index=False, sep="\t")
print(df_wide)
