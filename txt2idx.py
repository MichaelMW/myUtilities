#!/usr/bin/env python
# encoding: utf-8

## input a column of txt
## output cout the unique index of the txt,
## output cerr the dict: index -> txt. 

from sys import argv, stdin, stdout, stderr
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

txt2idx = dict()
txtList = list() 
for l in stdin.readlines():
	txt = l.strip().split()[0]
	txtList.append(txt)

# dict
for idx, txt in enumerate(set(txtList)):
	stderr.write(str(idx)+"\t"+txt+"\n")
	txt2idx[txt] = idx


# txt 2 idx
for txt in txtList:
	idx = txt2idx[txt]
	stdout.write(txt+"\t"+str(idx)+"\n")


