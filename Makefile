jars:
	wget https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.3.0-1.20/flink-sql-connector-kafka-3.3.0-1.20.jar
	mv flink-sql-connector-kafka-3.3.0-1.20.jar flink/
	wget https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/3.3.0-1.20/flink-connector-jdbc-3.3.0-1.20.jar
	mv flink-connector-jdbc-3.3.0-1.20.jar flink/
	wget https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.3/postgresql-42.7.3.jar
	mv postgresql-42.7.3.jar flink/