#/bin/$SHELL

CHART_NAME=$1

helm repo add dask https://helm.dask.org/    # add the Dask Helm chart repository
helm repo update                             # get latest Helm charts
# For single-user deployments, use dask/dask
helm install $CHART_NAME dask/dask               # deploy standard Dask chart

