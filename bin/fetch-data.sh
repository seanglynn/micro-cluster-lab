#/bin/$SHELL

URL=$1
DATASET_FILE_NAME=$2

#WGET Required
wget $URL -o datasets/$DATASET_FILE_NAME