import dlt
from pyspark.sql.functions import col, current_timestamp, upper


@dlt.table(
    name="table_b",
    comment="Transformed data from table_a with cleaning and enrichment",
)
@dlt.expect_or_drop("valid_id", "id IS NOT NULL")
@dlt.expect_or_drop("valid_name", "name IS NOT NULL")
def table_b():
    """
    Reads from table_a and applies transformations to produce table_b.

    Transformations applied:
    - Filters out rows where id or name is null (via expectations)
    - Converts the name column to uppercase
    - Adds a processed_at timestamp
    """
    return (
        dlt.read("table_a")
        .select(
            col("id"),
            upper(col("name")).alias("name"),
            col("value"),
            current_timestamp().alias("processed_at"),
        )
    )
