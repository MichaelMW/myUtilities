#!/usr/bin/env Rscript

# input infile, which is just the tsv, no header, no colnames; output to tsv
# eg. Rscript --vanilla qnorm.r data.tsv

args = commandArgs(trailingOnly=TRUE)


library(preprocessCore)

inFile=args[1]
outFile=paste(inFile,".qnormed.tsv", sep="")

# qnorm
qnorm <- function(df){
	df.qnorm = as.matrix(normalize.quantiles(df))	
	rownames(df.qnorm) = rownames(df)
	colnames(df.qnorm) = colnames(df)
	return(df.qnorm)
}

inMat <- as.matrix(read.table(file=inFile,header=F))
outMat <- qnorm(inMat)


write.table(outMat,sep="\t",file=outFile, quote = F,row.names = F, col.names = F)
