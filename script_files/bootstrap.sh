#!/bin/bash

hdfs namenode -format
service ssh start
if [ "$HOSTNAME" = node-master ]; then
    start-dfs.sh
    #start-master.sh
    cd /root/lab
    jupyter trust Dask-Yarn.ipynb
    jupyter trust Python-Spark.ipynb
    jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password='' 
    start-yarn.sh &
fi
#bash
while :; do :; done & kill -STOP $! && wait $!