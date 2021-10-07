#/bin/$SHELL

set -e

debug_container_name="debug-cluster-base"

echo "Deploying $debug_container_name"
docker build . --force-rm -t cluster-base 
docker run --name "debug-cluster-base" -d cluster-base

echo "Deploying $debug_container_name"
docker exec -it $debug_container_name bash