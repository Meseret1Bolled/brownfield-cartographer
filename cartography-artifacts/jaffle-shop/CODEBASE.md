# CODEBASE.md — `jaffle_shop`

_Generated: 2026-03-14T16:03:07.925204+00:00_
_System type: dbt data transformation project_

## Architecture Overview

`jaffle_shop` is a **dbt data transformation project** comprising `8` modules connected by `5` import dependencies. The data layer contains `9` datasets across `5` tracked transformations. The structural centre of gravity is `models/staging/stg_payments.sql`, `models/staging/stg_orders.sql`, `models/staging/stg_customers.sql`. No circular dependencies detected. 2 module(s) flagged as potential dead code.

## Critical Path

Top modules by PageRank (highest structural influence):

1. `models/staging/stg_payments.sql`
   - Purpose: Transform raw payment data from cents to dollars and standardize column names
   - PageRank: `0.17612` | Domain: `transformation` | Velocity: `0` commits (90d)
2. `models/staging/stg_orders.sql`
   - Purpose: Transforms raw order data into a structured staging table for analysis, standardizing column names and making order information ready for downstream processing.
   - PageRank: `0.17612` | Domain: `transformation` | Velocity: `0` commits (90d)
3. `models/staging/stg_customers.sql`
   - Purpose: Transforms raw customer data into a structured staging table for analysis, standardizing column names and making customer information ready for downstream processing.
   - PageRank: `0.13230` | Domain: `transformation` | Velocity: `0` commits (90d)
4. `dbt_project.yml`
   - Purpose: Configure dbt project settings and paths for data transformation pipeline
   - PageRank: `0.10309` | Domain: `configuration` | Velocity: `0` commits (90d)
5. `models/orders.sql`
   - Purpose: Transform payment data to show order-level breakdown by payment method and calculate total order amounts
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
  - Configure dbt project settings and paths for data transformation pipeline
  - LOC: `26` | PageRank: `0.10309` | Complexity: `0.0`
- `models/schema.yml`
  - Define data model schemas and validation rules for customers and orders tables
  - LOC: `82` | PageRank: `0.10309` | Complexity: `0.0`
### testing

- `models/staging/schema.yml`
  - Defines data quality tests and constraints for staging tables, ensuring data integrity by validating uniqueness, non-null values, and acceptable value ranges for key fields.
  - LOC: `31` | PageRank: `0.10309` | Complexity: `0.0`
### transformation

- `models/staging/stg_orders.sql`
  - Transforms raw order data into a structured staging table for analysis, standardizing column names and making order information ready for downstream processing.
  - LOC: `23` | PageRank: `0.17612` | Complexity: `5.0`
- `models/staging/stg_payments.sql`
  - Transform raw payment data from cents to dollars and standardize column names
  - LOC: `25` | PageRank: `0.17612` | Complexity: `5.0`
- `models/staging/stg_customers.sql`
  - Transforms raw customer data into a structured staging table for analysis, standardizing column names and making customer information ready for downstream processing.
  - LOC: `22` | PageRank: `0.13230` | Complexity: `5.0`
- `models/customers.sql` ⚠️dead-code-candidate
  - Create customer summary table with order history and lifetime value metrics
  - LOC: `69` | PageRank: `0.10309` | Complexity: `11.0`
- `models/orders.sql` ⚠️dead-code-candidate
  - Transform payment data to show order-level breakdown by payment method and calculate total order amounts
  - LOC: `56` | PageRank: `0.10309` | Complexity: `8.0`
