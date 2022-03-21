#!/bin/bash


## note the quotation marks. 
## ./pairWiseJaccard.sh "b2/*.bed"

inFiles=$1

getJaccard () {
	inA=$1
	inB=$2
	JAC=`bedtools jaccard -a <(sortBed -i $inA) -b <(sortBed -i $inB) | tail -n+2 | cut -f3`
}

f=($inFiles)
for ((i = 0; i < ${#f[@]}; i++)); do
	inA=${f[i]}
	echo -ne "$inA\t"
	#for ((j = i + 1; j < ${#f[@]}; j++)); do
	for ((j = 0; j < ${#f[@]}; j++)); do 
		inB=${f[j]}
		getJaccard $inA $inB
		echo -ne "\t$JAC"
	done
	echo 
done
