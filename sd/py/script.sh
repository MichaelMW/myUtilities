#!/bin/sh


## intended behavior
sds 	# will display all saved kw:dir
## load
sds d1 	# will cd into dir associated with kw=d1


sd d1 	# will save dir=pwd to kw=d1

## manage/delete
sd d1 [or wildcard] 	# will delete kw:dir glob by *wildcard



sd -a kw [dir]		add dir to kw. default dir = pwd
sd -c kw 			cd into kw dir. 

sd -d kw 			delete kw from list. support wildcard
sd -l [kw]			list dirs, support wildcard


s -> 	sd -c. cd into dir
sd -> 	sd -a. save dir. 
ss -> 	list dirs. 
ssd -> 	del kw from list. 
