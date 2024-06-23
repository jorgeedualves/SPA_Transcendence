#!/bin/bash

# Check if a container name argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <container_name>"
    exit 1
fi

CONTAINER_NAME="$1"

# Escape special characters in the container name using printf
ESCAPED_NAME=$(printf "%q" "$CONTAINER_NAME")

# Check if the container exists (assumes it's stopped)
if docker ps -a -q --filter "name=^/$ESCAPED_NAME$" | grep -q . ; then
    printf "Deleting container ${ESCAPED_NAME}...\n"
    docker rm ${ESCAPED_NAME}
else
    printf "Container ${ESCAPED_NAME} does not exist. No action needed.\n"
fi
