#/bin/$SHELL

JUPYTER_ENABLE_LAB=yes
CONTAINER_STORAGE_PATH=container_storage
NB_DIR=notebooks

#Require Jupyter

jupyter trust $NB_DIR=Bash-Interface.ipynb
jupyter trust $NB_DIR=Dask-Yarn.ipynb
jupyter trust $NB_DIR=Python-Spark.ipynb
jupyter trust $NB_DIR=Scala-Spark.ipynb
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password='' &

docker run --rm -p 10000:8888 -e JUPYTER_ENABLE_LAB=$JUPYTER_ENABLE_LAB -v "${PWD}/$CONTAINER_STORAGE_PATH":./ jupyter/datascience-notebook:latest
