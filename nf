#!/bin/bash

## desired behavior
# cat $inFile | nf # use tab as sep
# cat $inFile | nf -F ',' # use , as sep
# nf $inFile # use tab as sep
# nf $inFile -F',' # use , as sep

defaultSep=$'\t'
if test ! -t 0; then
	sep="${1:-$defaultSep}"
	awk -F"$sep" '{print NF}' 
else
	sep="${2:-$defaultSep}"
	awk -F"$sep" '{print NF}' $1
fi
