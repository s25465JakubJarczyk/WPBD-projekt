from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, IntegerType, StringType

# Tworzenie sesji Spark
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Schemat wiadomości JSON
product_schema = StructType() \
    .add("product_id", IntegerType()) \
    .add("name", StringType()) \
    .add("price", IntegerType())

# Czytanie ze strumienia Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "pg.public.products") \
    .option("startingOffsets", "earliest") \
    .load()

# Parsowanie JSON (pola "value" z Kafka to bajty)
df_parsed = df.selectExpr("CAST(value AS STRING) as json_str") \
    .select(from_json("json_str", StructType()
                      .add("after", product_schema)
                      .add("op", StringType())
                      ).alias("data")) \
    .select("data.after.*", "data.op") \
    .filter(col("op") == "c") \
    .filter(col("price") > 3000)

# Wyświetlanie na konsolę
query = df_parsed.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination()
