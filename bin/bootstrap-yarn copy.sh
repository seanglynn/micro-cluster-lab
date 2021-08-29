#!/bin/bash

hdfs namenode -format
service ssh start
if [ "$HOSTNAME" = node-master ]; then
    start-dfs.sh
    start-yarn.sh
    #start-master.sh
    cd /root/lab
fi
#bash
while :; do :; done & kill -STOP $! && wait $!