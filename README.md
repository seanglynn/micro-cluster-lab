# MicroDataCluster with Data API Using Docker (Dask/Spark, YARN, HDFS, MongoDB, FastAPI)

### Get Started
1. Register and Download geoip datasets from:
[geoip datasets downloads](https://www.maxmind.com/en/accounts/*/geoip/downloads). Files to download:
   - GeoLite2 City: CSV Format	
   - GeoLite2 Country: CSV Format	

2. Drop data into datasets folder:
```bash
datasets/public
datasets/private
```

3. [Exec Geolookup](https://github.com/seanglynn/micro-cluster-lab/blob/master/notebooks/GeoLookup.ipynb)
   - Geolocation data will be parsed, stored in memory for lookup and written out to Mongo.

4. [Exec PySparkYieldData](https://github.com/seanglynn/micro-cluster-lab/blob/master/notebooks/PySparkYieldData.ipynb)
   - Input dataset is joined with geolocation lookup DF and results are returned.

5. Hit API http://localhost:8002/
   - Query mongo data api to retreive results

### Project Folder Tree

```
├── docker-compose-complete.yml
├── docker-compose-dask.yml
├── docker-compose-spark.yml
├── Dockerfile
├── api
│   ├── server
    │   ├── models/
    │   └── routes/
    │   └── app.py
    │   └── database.py
│   ├── main.py
├── bin
│   ├── debug-cluster-base.sh
│   ├── fetch-data.sh
│   ├── restart-cluster-service.sh
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
Builds containers and spins up docker-compose cluster
```bash
./bin/restart-cluster-service.sh --all
```

### Create the compute container image
Manually build cluster base image
```bash
docker build . -t cluster-base
```

### Create the api container image
Manually build api image
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

```bash
# Get All Users in collection
http://localhost:8002/user

# Get Users within time range
http://localhost:8002/user?start_date=2014-10-11T17:02:54&end_date=2014-10-12T17:02:55

# Get OS Stats
http://localhost:8002/stats/os

# Get Browser Stats
http://localhost:8002/stats/browser


```


### Stopping the micro-cluster

```bash
docker-compose down
```


## Credit to aminelemaiz for developing YARN microcluster

For more details about this project please refer to [article](https://lemaizi.com/blog/creating-your-own-micro-cluster-lab-using-docker-to-experiment-with-spark-dask-on-yarn/)
