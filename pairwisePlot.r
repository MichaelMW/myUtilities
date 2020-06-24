#!/usr/bin/env Rscript

library("psych") 

## Collect arguments
args <- commandArgs(TRUE)
 
## Default setting when no arguments passed
if(length(args) < 1) {
	args <- c("--help")
	}
 
## Help section
if("--help" %in% args) {
	cat("
	plotPairwise.r using psych library.
	
	Arguments:
	--inFile=[inFile.tsv, please include a header]
	--main=[title of the plot, default is inFile]  
	--log=[base of log if exist, input as numeric, eg. e, 10, default is no log]
	--cor=[pearson or spearman, default is pearson]
	--format=[png or pdf, default is png]
	--help
	
	Example:
	pairwisePlot.r --inFile='test.tsv' --main='test title'; cor='spearman' \n\n")
	
	q(save="no")
	}
 
## Parse arguments (we expect the form --arg=value)
parseArgs <- function(x) strsplit(sub("^--", "", x), "=")
argsDF <- as.data.frame(do.call("rbind", parseArgs(args)))
argsL <- as.list(as.character(argsDF$V2))
names(argsL) <- argsDF$V1
 
## inFile default
if(is.null(argsL$inFile)) {
	cat("no input file! use --help for more info\n")
	q(save="no")
	}

## main default
if(is.null(argsL$main)) {
	argsL$main=argsL$inFile
	}
 
## log default
if(is.null(argsL$log)) {
	argsL$log="NA"
	}

## correlation method default
if(is.null(argsL$cor)) {
	argsL$cor="pearson"
	}

## output format default
if(is.null(argsL$format)) {
	argsL$format="png"
	}

inFile=argsL$inFile
main=argsL$main
useLog=argsL$log
corMethod=argsL$cor
format=argsL$format

outFile=paste(inFile,".pairWise.",format, sep="") 

cat("using inFile='",inFile,"'\nmain='",main,"'\nlog:",useLog,"\ncorMethod:",corMethod,"\noutFile='",outFile,"'\n",sep="")

# pairwise
pairwisePlot <- function(inFile, outFile, main, useLog, corMethod, format)
{
	mat<-as.matrix(read.table(inFile,header=T))
	if (useLog!="NA"){
		mat<-log(mat+1,as.numeric(useLog))
	}
	if (format=="pdf"){
		pdf(outFile)
	} else {
		png(outFile)
	}
	pairs.panels(mat, pch=".", method=corMethod, main=main)	
	dev.off()
}

pairwisePlot(inFile, outFile, main, useLog, corMethod, format)

