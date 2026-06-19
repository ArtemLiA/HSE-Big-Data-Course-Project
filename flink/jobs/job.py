from pyflink.table import EnvironmentSettings
from pyflink.table import TableEnvironment


env_settings = EnvironmentSettings.in_streaming_mode()
t_env = TableEnvironment.create(env_settings)

t_env.get_config().set("pipeline.name", "iot-flink-job")


# Чтение Kafka
t_env.execute_sql(
    """
    CREATE TABLE iot_events (
        device_id INT,
        event_time TIMESTAMP(3),
        temperature DOUBLE,
        humidity DOUBLE,
        WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'iot-messages',
        'properties.bootstrap.servers' = 'kafka:9092',
        'properties.group.id' = 'flink-iot',
        'scan.startup.mode' = 'earliest-offset',
        'format' = 'json',
        'json.timestamp-format.standard' = 'ISO-8601'
    )
    """
)


# Чтение справочника из PostgreSQL
t_env.execute_sql(
    """
    CREATE TABLE device_types (
        id INT,
        type_name STRING,
        PRIMARY KEY (id) NOT ENFORCED
    ) WITH (
        'connector' = 'jdbc',
        'url' = 'jdbc:postgresql://postgres:5432/iot_db',
        'table-name' = 'device_types',
        'username' = 'admin',
        'password' = 'admin',
        'lookup.cache.max-rows' = '1000',
        'lookup.cache.ttl' = '10s'
    )
    """
)


# Создаём таблицу для записи результата
t_env.execute_sql(
    """
    CREATE TABLE iot_aggregated (
        event_minute STRING,
        device_type STRING,
        avg_temperature DOUBLE,
        avg_humidity DOUBLE
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'iot-aggregated',
        'properties.bootstrap.servers' = 'kafka:9092',
        'format' = 'json'
    )
    """
)


# Считаем значения и записываем результат
t_env.execute_sql(
    """
    INSERT INTO iot_aggregated
    SELECT
        DATE_FORMAT(TUMBLE_START(event_time, INTERVAL '1' MINUTE), 'HH:mm') AS event_minute,
        dt.type_name,
        AVG(e.temperature) AS avg_temperature,
        AVG(e.humidity) AS avg_humidity
    FROM 
        iot_events e JOIN device_types dt
        ON e.device_id = dt.id
    GROUP BY
        TUMBLE(e.event_time, INTERVAL '1' MINUTE),
        dt.type_name
    """
)
