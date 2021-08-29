#/bin/bash

# 1. Ensure docker installed
# 2. Ensure snyke installed

IMAGE_FILE=$1
docker scan -f $IMAGE_FILE