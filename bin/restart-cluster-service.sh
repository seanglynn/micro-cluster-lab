#/bin/$SHELL

set -e

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

compose_yaml="docker-compose-${cluster}.yml"

echo "Clean-deploying: ${compose_yaml}"
docker system prune -f

docker build . --force-rm -t cluster-base 
docker-compose -f $compose_yaml up --build