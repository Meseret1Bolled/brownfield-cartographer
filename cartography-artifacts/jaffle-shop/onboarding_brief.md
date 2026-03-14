# FDE Day-One Onboarding Brief — `jaffle_shop`

_Generated: 2026-03-14T15:43:17.043582+00:00_
_System: dbt data transformation project_

## Five FDE Day-One Answers

### Q1. What is the primary data ingestion path? (trace from raw sources to first transformation)

The primary data ingestion path starts from the raw sources: raw_payments, raw_orders, raw_customers, and jaffle_shop. These are ingested into the staging layer through the transformation files stg_payments.sql, stg_orders.sql, and stg_customers.sql, which standardize and prepare the data for downstream use.

### Q2. What are the 3-5 most critical output datasets or endpoints?

The most critical output datasets are the final models: orders, customers, and jaffle_shop. These datasets represent the end result of the data transformation pipeline, aggregating and combining data from multiple sources for analytics and reporting purposes.

### Q3. What is the blast radius if the most critical module fails? (which downstream systems break)

If the most critical module, stg_payments.sql, fails, the blast radius would affect the orders and customers models, as they both depend on stg_payments. This would disrupt order financial analysis and customer lifetime value calculations, impacting downstream analytics and reporting.

### Q4. Where is the business logic concentrated vs distributed? (which modules/files own the core rules)

The business logic is concentrated in the transformation files, particularly in the staging layer (stg_payments.sql, stg_orders.sql, stg_customers.sql) and the final models (orders.sql, customers.sql). These files contain the core rules for data standardization, aggregation, and combination, while the configuration and testing files (dbt_project.yml, schema.yml) provide structure and validation.

### Q5. What has changed most frequently in the last 30 days? (git velocity map — likely pain points)

In the last 30 days, the most frequently changed files are dbt_project.yml, orders.sql, customers.sql, schema.yml, and stg_payments.sql. These files likely represent pain points in the codebase, with frequent modifications to project configuration, order and customer models, and data quality tests.

## Evidence Summary

- Repository: `jaffle_shop`
- System type: dbt data transformation project
- Module graph nodes: `8`
- Module graph edges: `5`
- Lineage datasets: `9`
- Lineage transformations: `5`
- Git analysis window: `90` days
- LLM-generated answers: `yes`

## Immediate Next Actions

1. Verify the top architectural hubs by navigating to their source files.
2. Validate upstream lineage for the highest-value sink datasets.
3. Inspect high-velocity files first — they're the most likely source of instability.
4. Review documentation drift flags before trusting any existing comments/docstrings.
5. Run `cartographer query <repo> --cartography-dir .cartography` to interactively explore.
