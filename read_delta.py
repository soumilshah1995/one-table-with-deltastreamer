from pyspark.sql import SparkSession

SPARK_VERSION = '3.4'
DELTA_VERSION = '2.4.0'  # Adjust the Delta version based on compatibility

# Use --packages and --conf options directly in PySpark code
spark = SparkSession.builder \
    .appName("DeltaReadExample") \
    .config('spark.sql.extensions', 'io.delta.sql.DeltaSparkSessionExtension') \
    .config('spark.sql.catalog.spark_catalog', 'org.apache.spark.sql.delta.catalog.DeltaCatalog') \
    .config('spark.jars.packages', f'io.delta:delta-core_2.12:{DELTA_VERSION}') \
    .getOrCreate()

# Read data from Delta table
delta_table_path = "file:///Users/soumilshah/IdeaProjects/SparkProject/DeltaStreamer/hudi/bronze_orders"
df = spark.read.format("delta").load(delta_table_path)

# Show DataFrame
df.show()