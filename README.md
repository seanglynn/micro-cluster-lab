# Micro-Cluster Lab Using Docker, To Experiment With Spark & Dask on Yarn

## Credit to aminelemaiz

For more details about this project please refer to [article](https://lemaizi.com/blog/creating-your-own-micro-cluster-lab-using-docker-to-experiment-with-spark-dask-on-yarn/)


### Get Started

Downloaded geoip datasets from:
[geoip datasets downloads](https://www.maxmind.com/en/accounts/*/geoip/downloads)

### Project Folder Tree

```
├── docker-compose.yml
├── Dockerfile
├── api
│   ├── server
    │   ├── models/
    │   └── routes/
    │   └── app.py
    │   └── database.py
│   ├── main.py
├── bin
│   ├── fetch-data.sh
│   ├── restart-etl-service.sh
│   ├── secure-image.sh
│   ├── run-adhoc-notebook.sh
├── confs
│   ├── config
│   ├── core-site.xml
│   ├── hdfs-site.xml
│   ├── mapred-site.xml
│   ├── requirements.req
│   ├── slaves
│   ├── spark-defaults.conf
│   └── yarn-site.xml
│   └── hadoop-env.xml
├── datasets
│   ├── private/
│   └── public
    │   ├── alice_in_wonderland.txt
    │   └── iris.csv
├── notebooks
│   ├── PySpark-Yield-Data.ipynb
│   ├── Dask-Yarn-Yield-Data.ipynb
└── script_files
    └── bootstrap.sh
```

### Run Microcluster

```bash
./bin/restart-etl-service.sh
```

### Create the compute container image

```bash
docker build . -t cluster-base
```

### Create the api container image

```bash
docker build ./api -t api
```

### UI's

YARN:
http://localhost:8088/cluster/nodes

Jupyter Notebook:
http://localhost:8888/

Mongo Express DB Viewer:
http://localhost:8081/db/local

Jupyter Notebook:
http://localhost:8888/

Jupyter Notebook:
http://localhost:8888/

UserGeo Mongo API:
http://localhost:8002/


### REST Requests

```
# Get All Users in collection
http://127.0.0.1:8002/user

# Get Users within time range
http://localhost:8002/user/?start_date=2014-10-11T17:02:54&end_date=2014-10-12T17:02:55

# Get OS Stats
http://127.0.0.1:8002/stats/os

# Get Browser Stats
http://127.0.0.1:8002/stats/browser



```


### Stopping the micro-cluster

```bash
docker-compose down
```


