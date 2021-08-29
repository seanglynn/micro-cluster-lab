#/bin/$SHELL

JUPYTER_ENABLE_LAB=yes


helm repo add dask https://helm.dask.org/    # add the Dask Helm chart repository
helm repo update                             # get latest Helm charts
# For single-user deployments, use dask/dask
helm install my-dask dask/dask               # deploy standard Dask chart

