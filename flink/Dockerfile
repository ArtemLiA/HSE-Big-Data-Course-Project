FROM flink:1.20.4

RUN apt-get update && apt-get install -y python3 python3-pip && pip3 install apache-flink
RUN ln -s /usr/bin/python3 /usr/bin/python

# Kafka connector
COPY flink-sql-connector-kafka-3.3.0-1.20.jar /opt/flink/lib/

# JDBC connector для PostgreSQL
COPY flink-connector-jdbc-3.3.0-1.20.jar /opt/flink/lib/

# Драйвер PostgreSQL
COPY postgresql-42.7.3.jar /opt/flink/lib/

# PyFlink job
COPY jobs/job.py /opt/flink/jobs/job.py
