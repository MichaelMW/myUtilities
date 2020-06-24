#!/usr/bin/env Rscript

library("randomForestSRC")

## Collect arguments
args <- commandArgs(TRUE)
 
## Default setting when no arguments passed
if(length(args) < 1) {
	args <- c("--help")
	}
 
## Help section
if("--help" %in% args) {
	cat("
	rf.r using randomForestSRC library.
	
	Arguments:
	--inFile=[inFile.tsv, please include a header]
	--outImp=[outFile for importance]
	--header=[use header, default is F]
	--label=[name of header used as the label column; if header=F, use something like V3 to specify the 3rd column]
	--ncpu=[number of cpus, default is 4]
	--ntree=[number of trees, default is 50]
	--nspilt=[number of splits, default is 3]
	--ntime=[number of time, default is 10 (speed up when row number is huge)]
	--importance=[show variable importance, default is T]

	--help
	
	Example:
	rf.r --inFile='test.tsv' --outImp='test.imp.tsv' --header='F' --label='V15' --importance=F \n\n")
	
	q(save="no")
	}
 
## Parse arguments (we expect the form --arg=value)
parseArgs <- function(x) strsplit(sub("^--", "", x), "=")
argsDF <- as.data.frame(do.call("rbind", parseArgs(args)))
argsL <- as.list(as.character(argsDF$V2))
names(argsL) <- argsDF$V1
 
## set defaults
if(is.null(argsL$inFile)) {
	cat("no input file! use --help for more info\n")
	q(save="no")
	}

if(is.null(argsL$label)) {
	cat("no label! use --help for more info\n")
	q(save="no")
	}

if(is.null(argsL$outImp)){
	argsL$outImp=paste(argsL$inFile,".imp",sep="")
	}
if(is.null(argsL$header)) {
	argsL$header="F"
	}

if(is.null(argsL$ncpu)) {
	argsL$ncpu=4
	}
 
if(is.null(argsL$ntree)) {
	argsL$ntree=50
	}

if(is.null(argsL$nsplit)) {
	argsL$nsplit=3
	}

if(is.null(argsL$ntime)) {
	argsL$ntime=10
	}

if(is.null(argsL$importance)) {
	argsL$importance="T"
	}

inFile=argsL$inFile
outImp=argsL$outImp
header=argsL$header
label=argsL$label
ncpu=as.integer(argsL$ncpu)
ntree=as.integer(argsL$ntree)
nsplit=as.integer(argsL$nsplit)
ntime=as.integer(argsL$ntime)
importance=argsL$importance



## main here
options(rf.cores = ncpu, mc.cores = ncpu)



cat("using inFile='",inFile,"'\nlabel='",label, "'\nncpu=",ncpu,"\nheader=",header,"\nimportance=",importance,"\n",sep="")

# pairwise
dat <- read.table(inFile, header=as.logical(header), sep="\t")
obj <- rfsrc(as.formula(paste(label," ~ .", sep="")), data = dat, ntree=ntree, nsplit = nsplit,ntime=ntime, importance=importance)

print(obj)
#obj$importance

write.table(obj$importance, file=outImp, sep="\t", quote = FALSE)
