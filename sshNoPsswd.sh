#!/bin/bash

# Usage: script_name user@server [-p port]

# Default SSH port
PORT=22
SSH_TARGET=""

# Flag to indicate if the next argument is the port number
NEXT_IS_PORT=false

# Parse arguments
for arg in "$@"; do
    if [ "$NEXT_IS_PORT" = true ]; then
        PORT=$arg
        NEXT_IS_PORT=false
    elif [ "$arg" = "-p" ]; then
        NEXT_IS_PORT=true
    elif [ -z "$SSH_TARGET" ]; then
        SSH_TARGET=$arg
    fi
done

echo "Using port: $PORT"
echo "SSH target: $SSH_TARGET"

# Check if SSH key exists, generate if not
if [ ! -f ~/.ssh/id_rsa.pub ]; then
    ssh-keygen -t rsa
fi

# Add public key to remote server's authorized_keys
ssh -p $PORT $SSH_TARGET mkdir -p .ssh
cat ~/.ssh/id_rsa.pub | ssh -p $PORT $SSH_TARGET 'cat >> .ssh/authorized_keys'
ssh -p $PORT $SSH_TARGET "chmod 700 .ssh; chmod 640 .ssh/authorized_keys"

