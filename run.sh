#!/bin/bash

./build_tf.py

$HADOOP_HOME/bin/hdfs namenode -format
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/bin/hdfs dfs -mkdir /user
$HADOOP_HOME/bin/hdfs dfs -mkdir /user/$USER
$HADOOP_HOME/bin/hdfs dfs -rm /user/$USER/index/*
$HADOOP_HOME/bin/hdfs dfs -rmdir /user/$USER/index
$HADOOP_HOME/bin/hdfs dfs -rm /user/$USER/articles/*
$HADOOP_HOME/bin/hdfs dfs -rmdir /user/$USER/articles
$HADOOP_HOME/bin/hdfs dfs -copyFromLocal articles hdfs://localhost:9000/user/$USER

$HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.0.0-alpha1.jar -mapper map.py -reducer reduce.py -input articles -output index -file map.py -file reduce.py 

$HADOOP_HOME/bin/hdfs dfs -copyToLocal hdfs://localhost:9000/user/$USER/index index
