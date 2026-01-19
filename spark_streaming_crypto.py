from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, FloatType, TimestampType

PROJECT_ID = "streaming-project-483410"
BUCKET_NAME = "trinhducan-spark-483410"
INPUT_PATH = f"gs://{BUCKET_NAME}/raw_data/" # Where Spark wait for new files

# 1. Create Spark Session
spark = SparkSession.builder \
    .appName("CryptoFileStreaming") \
    .getOrCreate()

# Reduce junk logs for better readability
spark.sparkContext.setLogLevel("WARN")

# 2. Define schema
schema = StructType() \
    .add("symbol", StringType()) \
    .add("priceUsd", FloatType()) \
    .add("timestamp", TimestampType())

# 3. Read STREAM from FILE (ReadStream)
print("Watching GCS for new files...")
raw_stream = spark.readStream \
    .format("json") \
    .schema(schema) \
    .option("maxFilesPerTrigger", 1) \
    .load(INPUT_PATH)

# Write to BigQuery
print("Writing to BigQuery...")
query = raw_stream.writeStream \
    .format("bigquery") \
    .option("table", f"{PROJECT_ID}:crypto_streaming_dataset.crypto_rates") \
    .option("checkpointLocation", f"gs://{BUCKET_NAME}/checkpoints/file_v1") \
    .option("temporaryGcsBucket", BUCKET_NAME) \
    .outputMode("append") \
    .start()

query.awaitTermination()
