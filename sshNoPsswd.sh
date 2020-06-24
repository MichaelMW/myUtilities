#!/bin/bash

# this script automatically at authorized key to remote server
if [ ! -f ~/.ssh/id_rsa.pub ]; then
	ssh-keygen -t rsa
fi

## $1 is user@server
ssh $1 mkdir -p .ssh
cat ~/.ssh/id_rsa.pub | ssh $1 'cat >> .ssh/authorized_keys'
ssh $1 "chmod 700 .ssh; chmod 640 .ssh/authorized_keys"

