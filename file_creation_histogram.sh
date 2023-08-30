#!/usr/bin/env bash

# file_creation_histogram.sh
# 
# Plot a histogram of file creation dates within a specified directory.
# 
# Dependencies:
# - bashplotlib (install with 'pip install bashplotlib')
# 
# Usage:
#   ./file_creation_histogram.sh [DIRECTORY] [FILEPATTERN] [BINS] [USE_CURRENT_TIME]
# 
# Parameters:
#   DIRECTORY   : The root directory to start the search. Default is current directory.
#   FILEPATTERN: The file pattern to search for. Default is all files (*).
#   BINS       : Number of bins for the histogram. Default is 100.
#	USE_CURRENT_TIME 	: Include current time. Default to 1 as True.
#	
# 
# Example:
#   ./file_creation_histogram.sh ./data/ "*.gz" 50
#   This will search for all .gz files in the ./data/ directory and plot the histogram with 50 bins.
# 
# Author: Michael Wang
# Date: 8/30/23

# Check if bashplotlib is installed
if ! command -v hist &> /dev/null; then
    echo "bashplotlib is not installed. Install it using 'pip install bashplotlib'."
    exit 1
fi

# Defaults
INKW=${1:-"."}          	# input directory
FILEPATTERN=${2:-"*"}   	# file pattern to search for
BINS=${3:-"100"}        	# number of bins
USE_CURRENT_TIME=${4:-"1"}	# include current time, default to 1 as yes. 

# Determine OS and set the appropriate stat command
if [[ "$OSTYPE" == "darwin"* ]]; then
	STAT_CMD="stat -f '%m'"
else
    STAT_CMD="stat --format '%Y'"
fi

if [ $USE_CURRENT_TIME -eq 1 ]; then
	# Collect timestamps and plot histogram with current time
	(find $INKW -type f -name "$FILEPATTERN" -print0 | xargs -0 $STAT_CMD | tr -d "'"  ; date +%s) | hist -b $BINS
else
	# Collect timestamps and plot histogram
	find $INKW -type f -name "$FILEPATTERN" -print0 | xargs -0 $STAT_CMD  | tr -d "'"  | hist -b $BINS
fi

