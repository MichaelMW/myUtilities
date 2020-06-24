#!/usr/bin/env python


##### convert values to ranks, tie breaker as average #####
def rank_simple(vector):
    return sorted(range(len(vector)), key=vector.__getitem__)


def rankdata(a, sep):
    n = len(a)
    ivec = rank_simple(a)
    svec = [a[rank] for rank in ivec]
    sumranks = 0
    dupcount = 0
    newarray = [0]*n
    for i in range(n):
        sumranks += i
        dupcount += 1
        if i == n-1 or svec[i] != svec[i+1]:
            averank = sumranks / float(dupcount) + 1
            for j in range(i-dupcount+1, i+1):
                newarray[ivec[j]] = str(averank)
            sumranks = 0
            dupcount = 0
    return sep.join(newarray)


from sys import argv, stdin, stdout
from signal import signal, SIGPIPE, SIG_DFL
import argparse
signal(SIGPIPE, SIG_DFL)

# parse args
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inVals", help="input values")
parser.add_argument("-d", "--delimiter", default="\n",
                    help="used to split and join input and output")
args = parser.parse_args()
sep = args.delimiter

inData = [float(i) for i in list(stdin.readlines())]
print(rankdata(inData, sep=sep))
