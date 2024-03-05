![Screenshot 2024-03-04 at 7 47 52 PM](https://github.com/soumilshah1995/one-table-with-deltastreamer/assets/39345855/932b7fc1-ecc2-4fba-8319-f498b757a3ea)


### Download the jar from google drive 
Link : https://drive.google.com/drive/folders/1FQw8xljm9NRE9_BCoHSzpauH88FzRJAr?usp=share_link

# Spark Submit Command 
```
spark-submit \
    --class org.apache.hudi.utilities.streamer.HoodieStreamer \
    --packages 'org.apache.hudi:hudi-spark3.4-bundle_2.12:0.14.0' \
    --properties-file spark-config.properties \
    --master 'local[*]' \
    --executor-memory 1g \
    --jars /Users/soumilshah/IdeaProjects/SparkProject/DeltaStreamer/jar/hudi-extensions-0.1.0-SNAPSHOT-bundled.jar,/Users/soumilshah/IdeaProjects/SparkProject/DeltaStreamer/jar/hudi-java-client-0.14.0.jar \
     /Users/soumilshah/IdeaProjects/SparkProject/DeltaStreamer/jar/hudi-utilities-slim-bundle_2.12-0.14.0.jar \
    --table-type COPY_ON_WRITE \
    --target-base-path 'file:///Users/soumilshah/IdeaProjects/SparkProject/DeltaStreamer/hudi/bronze_orders'  \
    --target-table bronze_orders \
    --op UPSERT \
    --enable-sync \
    --sync-tool-classes 'io.onetable.hudi.sync.OneTableSyncTool' \
    --source-limit 4000000 \
    --source-ordering-field ts \
    --source-class org.apache.hudi.utilities.sources.CsvDFSSource \
    --hoodie-conf 'hoodie.datasource.write.recordkey.field=order_id' \
    --hoodie-conf 'hoodie.datasource.write.partitionpath.field=state' \
    --hoodie-conf 'hoodie.datasource.write.precombine.field=ts' \
    --hoodie-conf 'hoodie.streamer.source.dfs.root=file://///Users/soumilshah/IdeaProjects/SparkProject/DeltaStreamer/sampledata/orders' \
    --hoodie-conf 'hoodie.deltastreamer.csv.header=true' \
    --hoodie-conf 'hoodie.deltastreamer.csv.sep=\t' \
    --hoodie-conf 'hoodie.onetable.formats.to.sync=DELTA,ICEBERG' \
    --hoodie-conf 'hoodie.onetable.target.metadata.retention.hr=168'

```


# Read as Delta 
```
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
```
