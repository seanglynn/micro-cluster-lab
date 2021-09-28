FROM ubuntu:bionic

# showing to hadoop and spark where to find java!
ENV JAVA_HOME /usr/lib/jvm/java-1.8.0-openjdk-amd64/jre
# after downloading hadoop (a bit further) we have to inform any concerned
# app where to find it
ENV HADOOP_HOME /opt/hadoop
# same for the hadoop configuration
ENV HADOOP_CONF_DIR /opt/hadoop/etc/hadoop
# and same for spark
ENV SPARK_HOME /opt/spark

ENV PATH="${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin:${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${PATH}"

ENV HADOOP_VERSION=3.2.2
ENV SPARK_VERSION=3.1.2
ENV PYSPARK_DRIVER_PYTHON=jupyter
ENV PYSPARK_DRIVER_PYTHON_OPTS='notebook'

# showing pyspark which "python" command to use
ENV PYSPARK_PYTHON=python3

# Elephant props
ENV HDFS_NAMENODE_USER=root
ENV HDFS_DATANODE_USER=root
ENV HDFS_SECONDARYNAMENODE_USER=root
ENV YARN_RESOURCEMANAGER_USER=root
ENV YARN_NODEMANAGER_USER=root

# OS props
RUN apt-get update && \
    apt-get install -y wget nano openjdk-8-jdk ssh openssh-server build-essential
RUN apt update && apt install -y python3 python3-pip python3-dev libssl-dev libffi-dev libpq-dev nodejs curl bzip2 \
    && curl -sSL https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -bfp /usr/local \
    && rm -rf /tmp/miniconda.sh \
    && conda install -y python=3 \
    && conda update conda \
    && apt-get -qq -y remove curl bzip2 \
    && apt-get -qq -y autoremove \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /var/log/dpkg.log \
    && conda clean --all --yes \
    && conda config --append channels conda-forge

ENV PATH /opt/conda/bin:$PATH

# Dask props
ENV DASK_VERSION=0.8.0

# Jupyter deps
COPY confs/requirements.req /
RUN conda install --file requirements.req
RUN conda install -y dask[bag]==${DASK_VERSION} 
RUN conda install -y toree
RUN conda install -y dask_labextension
RUN python3 -m bash_kernel.install

# Dask deps
RUN conda install -y cmake \
    cytoolz \
    lz4 \
    numpy \
    pandas \
    ipywidgets \
    cachey \
    streamz \
    dask-labextension \
    jupyter-server-proxy 
    # numpy==1.21.1 \
    # pandas==1.3.0 \

# RUN apt install -y nodejs npm conda
# RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
# RUN chmod +x Miniconda3-latest-Linux-x86_64.sh
RUN conda install -y npm nodejs
RUN jupyter labextension install dask-labextension

RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    mkdir -p /usr/local/bin && \
    mv ./kubectl /usr/local/bin/kubectl && \
    chmod +x /usr/local/bin/kubectl && \
    kubectl version --client

RUN wget -P /tmp/ https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz
RUN tar xvf /tmp/hadoop-${HADOOP_VERSION}.tar.gz -C /tmp && \
  mv /tmp/hadoop-${HADOOP_VERSION} /opt/hadoop

RUN wget -P /tmp/ https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.2.tgz
RUN tar xvf /tmp/spark-${SPARK_VERSION}-bin-hadoop3.2.tgz -C /tmp && \
    mv /tmp/spark-${SPARK_VERSION}-bin-hadoop3.2 ${SPARK_HOME}

RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
  cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
  chmod 600 ~/.ssh/authorized_keys
COPY confs/config /root/.ssh
RUN chmod 600 /root/.ssh/config


COPY confs/*.xml /opt/hadoop/etc/hadoop/
COPY confs/hadoop-env.sh /opt/hadoop/etc/hadoop/
COPY confs/slaves /opt/hadoop/etc/hadoop/
COPY script_files/bootstrap.sh /

ENV JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64
COPY confs/spark-defaults.conf ${SPARK_HOME}/conf

RUN apt install -y unzip && \
  rm -rf /tmp/*spark*gz

EXPOSE 9000
EXPOSE 7077
EXPOSE 4040
EXPOSE 8020
EXPOSE 22

RUN mkdir -p /root/lab/datasets
COPY datasets/public/* /root/lab/datasets/
COPY datasets/private/* /root/lab/datasets/
COPY notebooks/* /root/lab/

ENTRYPOINT ["/bin/bash", "bootstrap.sh"]