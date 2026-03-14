# FDE Day-One Onboarding Brief — `jaffle_shop`

_Generated: 2026-03-14T16:03:07.932006+00:00_
_System: dbt data transformation project_

## Five FDE Day-One Answers

### Q1. What is the primary data ingestion path? (trace from raw sources to first transformation)

The primary data ingestion path starts with raw sources (raw_payments, raw_orders, raw_customers, jaffle_shop) flowing through staging transformations in the staging directory. The first transformation occurs in files like /tmp/cartographer_zl19dzgk/repo/models/staging/stg_payments.sql, /tmp/cartographer_zl19dzgk/repo/models/staging/stg_orders.sql, and /tmp/cartographer_zl19dzgk/repo/models/staging/stg_customers.sql, which standardize column names and prepare data for downstream processing.

### Q2. What are the 3-5 most critical output datasets or endpoints?

The three most critical output datasets are orders, customers, and jaffle_shop. These are identified as data sinks (out-degree=0) in the summary, meaning they serve as final destinations for transformed data rather than feeding other processes.

### Q3. What is the blast radius if the most critical module fails? (which downstream systems break)

If /tmp/cartographer_zl19dzgk/repo/models/staging/stg_payments.sql fails, it would break the stg_payments dataset, which is a direct dependency for both /tmp/cartographer_zl19dzgk/repo/models/orders.sql and /tmp/cartographer_zl19dzgk/repo/models/customers.sql. This would cascade to prevent the creation of the orders and customers final datasets, effectively halting the entire transformation pipeline.

### Q4. Where is the business logic concentrated vs distributed? (which modules/files own the core rules)

The business logic is concentrated in the transformation files within /tmp/cartographer_zl19dzgk/repo/models/staging/ and the main models directory. The staging files handle data standardization and basic transformations, while files like /tmp/cartographer_zl19dzgk/repo/models/orders.sql and /tmp/cartographer_zl19dzgk/repo/models/customers.sql contain more complex business logic for calculating order breakdowns and customer lifetime value metrics.

### Q5. What has changed most frequently in the last 30 days? (git velocity map — likely pain points)

Based on the high-velocity files from the last 30 days, /tmp/cartographer_zl19dzgk/repo/dbt_project.yml, /tmp/cartographer_zl19dzgk/repo/models/orders.sql, and /tmp/cartographer_zl19dzgk/repo/models/customers.sql have seen the most recent changes. These files likely represent the core transformation logic and project configuration, indicating they are active development areas and potential pain points for ongoing maintenance.

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
