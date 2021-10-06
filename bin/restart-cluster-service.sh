#/bin/$SHELL

case $1 in
    -a|--all) cluster="complete"            
    ;;
    -d|--dask) cluster="dask"   
    ;;
    -s|--spark) cluster="spark"           
    ;;
    *) echo "Cluster type must by passed via flag --all/--dask/--spark" 
    echo "Usage: ./bin/restart-cluster-service.sh [-a/-d/-s]"
    exit 1
    ;;
esac
shift

echo docker-compose-${cluster}.yml
docker build . -t cluster-base
docker-compose -f docker-compose-${cluster}.yml up --build