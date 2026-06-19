# Проект по курсу "Алгоритмы обработки больших данных"


## Структура проекта
- `producer` -> генератор сообщений от IoT-устройств с Kafka producer
- `sql` -> DDL и DML-скрипты для создания и заполнения справочника с IoT-устройствами
- `flink` -> Flink-приложение
  -  `jobs/job.py` -> основная Job'а для сбора поминутных статистик по устройствам
- `Makefile` -> Makefile для скачивания необходимых JAR-файлов для Flink


## Запуск приложения

### Скачивание JAR-файлов

Для работы с PostgreSQL и Kafka с использованием Table API и SQL в Apache Flink необходимо сначала скачать необходимые JAR-файлы. Сделать это при помощи make:
```bash
make jars
```

### Запуск контейнеров

Для запуска контейнеров достаточно воспользоваться `docker compose`:
```bash
docker compose up --build
```

### Создание топиков в Kafka
В моём случае у Kafka была установлена настройка:
```bash
auto.create.topics.enable=true
```

По этой причине, топики при необходимости создавались автоматически.

Если данная опция отключена, то необходимо отдельно создать два топика:
- `iot-messages` -> сообщения от IoT-устройств
- `iot-aggregated` -> статистики за минуту от IoT-устройств

Для этого сначала необходимо зайти в контейнер Kafka:
```bash
docker exec -it kafka bash
```

И затем создать оба топика:
```bash
kafka-topics --create \
  --topic iot-events \
  --bootstrap-server kafka:9092 \
  --partitions 1 \
  --replication-factor 1
```

```bash
```bash
kafka-topics --create \
  --topic iot-aggregated \
  --bootstrap-server kafka:9092 \
  --partitions 1 \
  --replication-factor 1
```


### Запуск Flink Job

Заходим в контейнер Flink:
```bash
docker exec -it jobmanager bash
```

И затем запускаем Job'у:
```bash
flink run -py /opt/flink/jobs/job.py
```

## Комментарий от автора

В моей работе есть ограничения:
1. PostgreSQL используется как статический справочник (без CDC)
2. Может потребоваться создавать топики вручную
