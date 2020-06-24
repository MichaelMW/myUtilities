#!/usr/bin/env python
# encoding: utf-8

import argparse
parser = argparse.ArgumentParser()


parser.add_argument('-a', dest="kw", help='sd -a kw will save cwd into kw.')
parser.add_argument('-c', dest="kw", version='%(prog)s 1.0')
args = parser.parse_args()

print args.simple_value



sd -a kw [dir]      add dir to kw. default dir = pwd
sd -c kw            cd into kw dir.

sd -d kw            delete kw from list. support wildcard
sd -l [kw]          list dirs, support wildcard


s ->    sd -c. cd into dir
sd ->   sd -a. save dir.
ss ->   list dirs.
ssd ->  del kw from list.

