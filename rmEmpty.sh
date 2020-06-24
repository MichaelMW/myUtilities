#!/bin/bash

# this script rm empty files in the CWD
for f in *; do
	if [ ! -s $f ]; then
		rm $f
	fi
done
