#!/bin/bash


if [ -z "$1" ]; then
    echo "echo no port number supplied, use 2888 as default"
	portID=2888
else
	echo "port ID supplied = $1"
	portID=$1
fi

echo "server host at:"
echo `getMyIP.sh`":"$portID

#python -m SimpleHTTPServer $portID  ##python2 
python -m http.server $portID ## python3



