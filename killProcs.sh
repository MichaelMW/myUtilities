#!/bin/bash

# input keywords in ps, kill them all
# eg. killProcs.sh bash
#ps -u mengchi | grep $1 | cut -f1 -d" " | xargs kill -KILL
ps -u mengchi | cut -f1 -d" " | xargs kill -KILL

