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
# with this we can run all hadoop and spark scripts and commands directly from the shell
# without using the absolute path
ENV PATH="${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin:${SPARK_HOME}/bin:${SPARK_HOME}/sbin:${PATH}"
# just informing the hadoop version, this isn't really necessary
ENV HADOOP_VERSION 3.2.2
# if you happend to run pyspark from shell, it will launch it on a Jupyter Notebook
# this is just two fancy lines, really no need for it
ENV PYSPARK_DRIVER_PYTHON=jupyter
ENV PYSPARK_DRIVER_PYTHON_OPTS='notebook'
# showing pyspark which "python" command to use
ENV PYSPARK_PYTHON=python3

ENV HDFS_NAMENODE_USER=root
ENV HDFS_DATANODE_USER=root
ENV HDFS_SECONDARYNAMENODE_USER=root
ENV YARN_RESOURCEMANAGER_USER=root
ENV YARN_NODEMANAGER_USER=root

RUN apt-get update && \
    apt-get install -y wget nano openjdk-8-jdk ssh openssh-server build-essential
RUN apt update && apt install -y python3 python3-pip python3-dev build-essential libssl-dev libffi-dev libpq-dev 


COPY confs/requirements.req /
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.req
RUN pip3 install dask[bag] --upgrade
RUN pip3 install --upgrade toree
RUN pip3 install --upgrade jupyter-server-proxy 
RUN python3 -m bash_kernel.install

RUN wget -P /tmp/ https://archive.apache.org/dist/hadoop/common/hadoop-3.2.2/hadoop-3.2.2.tar.gz
RUN tar xvf /tmp/hadoop-3.2.2.tar.gz -C /tmp && \
  mv /tmp/hadoop-3.2.2 /opt/hadoop

RUN wget -P /tmp/ https://dlcdn.apache.org/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz
RUN tar xvf /tmp/spark-3.1.2-bin-hadoop3.2.tgz -C /tmp && \
    mv /tmp/spark-3.1.2-bin-hadoop3.2 ${SPARK_HOME}

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