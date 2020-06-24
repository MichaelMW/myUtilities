#!/usr/bin/env python
from sys import stdin, stderr
from numpy import std, mean, median
from signal import signal, SIGPIPE, SIG_DFL


signal(SIGPIPE,SIG_DFL)

List=[]
failed = 0
for line in stdin.readlines():
	try:
		List.append(float(line.strip()))
	except ValueError:
		failed += 1
		pass

print("#:{}\nsum:{}\nmin:{}\nmax:{}\nmean:{}\nmedian:{}\nstd:{}\n".format(len(List),sum(List),min(List),max(List),mean(List),median(List),std(List)))

stderr.write("failed:{}\n".format(failed))
