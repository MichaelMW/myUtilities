#!/bin/bash

sciNumber=$1
roundby=$2
cutoff=-308

# only input number? default roundby=2
if [ $# -eq 1 ]; then
    roundby=2
fi


# round up for normal number
function roundup {
	echo `LC_ALL=C /usr/bin/printf "%.*f\n" $2 $1`
}

# is a number?
if [[ $sciNumber =~ ^[0-9\.Ee\-]+$ ]]; then

	# is a sci number?
	if [[ $sciNumber == *[eE]* ]]; then
		number=`echo $sciNumber | awk -F [eE] '{print $1}'`
		sci=`echo $sciNumber | awk -F [eE] '{print $2}'`
		
		# less then cutoff?
		if [ $sci -lt $cutoff ]; then
			output=0
		else
			output=`roundup $number $2`"E$sci"
		fi
	# not a sci number
	else
		output=`roundup $sciNumber $2`
	fi

# not a number
else
   	output=$sciNumber
fi

echo $output
