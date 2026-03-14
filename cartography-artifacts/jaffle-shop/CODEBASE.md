# CODEBASE.md — `jaffle_shop`

_Generated: 2026-03-14T15:43:17.038112+00:00_
_System type: dbt data transformation project_

## Architecture Overview

`jaffle_shop` is a **dbt data transformation project** comprising `8` modules connected by `5` import dependencies. The data layer contains `9` datasets across `5` tracked transformations. The structural centre of gravity is `models/staging/stg_payments.sql`, `models/staging/stg_orders.sql`, `models/staging/stg_customers.sql`. No circular dependencies detected. 2 module(s) flagged as potential dead code.

## Critical Path

Top modules by PageRank (highest structural influence):

1. `models/staging/stg_payments.sql`
   - Purpose: Transforms raw payment data by converting amounts to dollars and standardizing column names for downstream use
   - PageRank: `0.17612` | Domain: `transformation` | Velocity: `0` commits (90d)
2. `models/staging/stg_orders.sql`
   - Purpose: Transforms raw order data into a standardized staging table with consistent column naming for downstream analytics
   - PageRank: `0.17612` | Domain: `transformation` | Velocity: `0` commits (90d)
3. `models/staging/stg_customers.sql`
   - Purpose: Transforms raw customer data into a standardized staging table with consistent column naming for downstream analytics
   - PageRank: `0.13230` | Domain: `transformation` | Velocity: `0` commits (90d)
4. `dbt_project.yml`
   - Purpose: Configures the dbt project structure and settings for data transformation workflows
   - PageRank: `0.10309` | Domain: `configuration` | Velocity: `0` commits (90d)
5. `models/orders.sql`
   - Purpose: Aggregates payment data by payment method for each order to enable detailed order financial analysis
   - PageRank: `0.10309` | Domain: `transformation` | Velocity: `0` commits (90d)

## Data Sources & Sinks

### Sources
- `raw_payments`
- `raw_orders`
- `raw_customers`
- `jaffle_shop`

### Sinks
- `orders`
- `customers`
- `jaffle_shop`

## Known Debt

### Circular Dependencies
- No circular dependencies detected

### Documentation Drift
- No documentation drift flags recorded

## High-Velocity Files

Files with most commits in the last 90 days (likely pain points):
1. `dbt_project.yml` — `0` commits
2. `models/orders.sql` — `0` commits
3. `models/customers.sql` — `0` commits
4. `models/schema.yml` — `0` commits
5. `models/staging/stg_payments.sql` — `0` commits
6. `models/staging/stg_orders.sql` — `0` commits
7. `models/staging/schema.yml` — `0` commits
8. `models/staging/stg_customers.sql` — `0` commits

## Module Purpose Index

### configuration

- `dbt_project.yml`
  - Configures the dbt project structure and settings for data transformation workflows
  - LOC: `26` | PageRank: `0.10309` | Complexity: `0.0`
### testing

- `models/schema.yml`
  - Defines data models with documentation and validation rules for data quality assurance
  - LOC: `82` | PageRank: `0.10309` | Complexity: `0.0`
- `models/staging/schema.yml`
  - Defines data quality tests and constraints for staging tables to ensure data integrity before transformation
  - LOC: `31` | PageRank: `0.10309` | Complexity: `0.0`
### transformation

- `models/staging/stg_orders.sql`
  - Transforms raw order data into a standardized staging table with consistent column naming for downstream analytics
  - LOC: `23` | PageRank: `0.17612` | Complexity: `5.0`
- `models/staging/stg_payments.sql`
  - Transforms raw payment data by converting amounts to dollars and standardizing column names for downstream use
  - LOC: `25` | PageRank: `0.17612` | Complexity: `5.0`
- `models/staging/stg_customers.sql`
  - Transforms raw customer data into a standardized staging table with consistent column naming for downstream analytics
  - LOC: `22` | PageRank: `0.13230` | Complexity: `5.0`
- `models/customers.sql` ⚠️dead-code-candidate
  - Combines customer information with their order history and lifetime value for customer analytics
  - LOC: `69` | PageRank: `0.10309` | Complexity: `11.0`
- `models/orders.sql` ⚠️dead-code-candidate
  - Aggregates payment data by payment method for each order to enable detailed order financial analysis
  - LOC: `56` | PageRank: `0.10309` | Complexity: `8.0`
