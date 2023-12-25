#!/bin/bash

# This script automatically adds an authorized key to a remote server

# Usage: script_name user@server [-p port]

# Default SSH port
PORT=22

# Parse options
while getopts ":p:" opt; do
  case ${opt} in
    p )
      PORT=$OPTARG
      ;;
    \? )
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    : )
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

# Assign user@server to a variable
SSH_TARGET=$1

# Check if SSH key exists, generate if not
if [ ! -f ~/.ssh/id_rsa.pub ]; then
    ssh-keygen -t rsa
fi

# Add public key to remote server's authorized_keys
ssh -p $PORT $SSH_TARGET mkdir -p .ssh
cat ~/.ssh/id_rsa.pub | ssh -p $PORT $SSH_TARGET 'cat >> .ssh/authorized_keys'
ssh -p $PORT $SSH_TARGET "chmod 700 .ssh; chmod 640 .ssh/authorized_keys"

