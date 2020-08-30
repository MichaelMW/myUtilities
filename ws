#!/bin/bash

## check who's online and sort by idel time in seconds
who -s | perl -lane 'print "$F[1]\t$F[0]\t" . 86400 * -A "/dev/$F[1]"' | sort -nk3
