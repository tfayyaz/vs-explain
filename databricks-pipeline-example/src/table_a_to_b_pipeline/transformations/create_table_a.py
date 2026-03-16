import dlt
from pyspark.sql.functions import col


@dlt.table(
    name="table_a",
    comment="Source table ingested from raw data",
)
@dlt.expect_or_drop("valid_id", "id IS NOT NULL")
def table_a():
    """
    Ingests raw data into table_a using Auto Loader.

    This reads JSON files from a cloud storage path and
    automatically detects the schema.
    """
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .option("cloudFiles.inferColumnTypes", "true")
        .load("/mnt/raw-data/table_a/")
        .select(
            col("id").cast("long"),
            col("name").cast("string"),
            col("value").cast("double"),
        )
    )
