# Table A to Table B Pipeline

An example Databricks Declarative Automation Bundle that demonstrates a simple ETL pipeline reading from `table_a` and writing to `table_b`.

## Project Structure

```
databricks-pipeline-example/
├── databricks.yml                          # Bundle configuration
├── pyproject.toml                          # Python project metadata
├── resources/
│   ├── table_a_to_b.pipeline.yml           # Pipeline resource definition
│   └── daily_job.job.yml                   # Scheduled job definition
└── src/
    └── table_a_to_b_pipeline/
        └── transformations/
            ├── create_table_a.py           # Source table (Auto Loader ingestion)
            └── table_a_to_b.py             # Transformation: table_a → table_b
```

## What This Pipeline Does

1. **table_a** — Ingests raw JSON data from cloud storage using Auto Loader with automatic schema detection
2. **table_b** — Reads from `table_a` and applies:
   - Data quality checks (drops rows with null `id` or `name`)
   - Converts `name` to uppercase
   - Adds a `processed_at` timestamp

## Pipeline Graph

```
  /mnt/raw-data/table_a/ (JSON)
          │
          ▼
     ┌─────────┐
     │ table_a  │  (streaming ingestion via Auto Loader)
     └────┬────┘
          │
          ▼
     ┌─────────┐
     │ table_b  │  (transformed + quality-checked)
     └─────────┘
```

## Prerequisites

- Databricks CLI v0.205+ (`databricks --version`)
- A Databricks workspace with Unity Catalog enabled
- Authentication configured (`databricks auth login`)

## Usage

```bash
# Validate the bundle configuration
databricks bundle validate

# Deploy to your dev workspace
databricks bundle deploy --target dev

# Run the pipeline
databricks bundle run table_a_to_b_pipeline --target dev

# Check pipeline status
databricks bundle summary --target dev

# Tear down deployed resources
databricks bundle destroy --target dev
```

## Customization

- **Change data source**: Edit `create_table_a.py` to point to your actual data path
- **Add transformations**: Add new `@dlt.table` functions in the `transformations/` folder
- **Schedule**: Edit `daily_job.job.yml` to change the cron schedule (currently paused for dev)
- **Target catalog/schema**: Update `variables` in `databricks.yml`
