# FDE Day-One Onboarding Brief — `ol-data-platform`

_Generated: 2026-03-14T20:26:47.076596+00:00_
_System: dbt data transformation project_

## Five FDE Day-One Answers

### Q1. What is the primary data ingestion path? (trace from raw sources to first transformation)

The primary data ingestion path begins with raw sources like user_course_roles, platforms, legacy_edx_certificate_revision_mapping, open_learning, edxorg_raw_data_archive, and edxorg_raw_tracking_logs, which feed into staging models such as stg__zendesk__ticket_field.sql and stg__micromasters__app__postgres__auth_user.sql. These staging models then transform the raw data into intermediate and dimensional models, with the most critical ingestion point being the tracking logs user_activity files across multiple platforms (mitxonline, mitxresidential, mitxpro, edxorg). The ingestion pipeline appears to be centralized around the DBT models in the staging directory, with tracking logs being the most heavily processed data source.

### Q2. What are the 3-5 most critical output datasets or endpoints?

The 3-5 most critical output datasets are the dimensional/dim_course_content.sql model which consolidates course structure data, the intermediate/mitxonline/int__mitxonline__users.sql model which creates unified user profiles, and the reporting/_reporting__models.yml configuration which likely drives business intelligence outputs. Additionally, the migration/edxorg_to_mitxonline_enrollments.sql model appears critical for cross-platform enrollment data synchronization. The tracking logs user_activity models across all platforms are also essential outputs for behavioral analytics.

### Q3. What is the blast radius if the most critical module fails? (which downstream systems break)

If the most critical module (stg__mitxonline__openedx__tracking_logs__user_activity.sql) fails, the blast radius would affect all downstream analytics and reporting that depend on user behavior data, including the intermediate/mitxonline/int__mitxonline__users.sql model and any reporting models that consume user activity data. The failure would also impact the dimensional/dim_course_content.sql model since it relies on user activity data for course engagement metrics. All business intelligence dashboards and analytics dependent on user behavior tracking would be compromised.

### Q4. Where is the business logic concentrated vs distributed? (which modules/files own the core rules)

The business logic is concentrated in the intermediate models, particularly int__mitxonline__users.sql and int__mitxonline__programs.sql, which handle user profile unification and program-level aggregation respectively. The staging models contain transformation logic but are more focused on data cleaning and preparation. The reporting models likely contain the final business logic for presentation and analytics, while the dimensional models primarily serve as data warehouses for consumption.

### Q5. What has changed most frequently in the last 30 days? (git velocity map — likely pain points)

Based on the velocity map, the most frequently changing files in the last 30 days are reporting/_reporting__models.yml, migration/edxorg_to_mitxonline_enrollments.sql, and the docker-compose.yaml configuration file. The CLI interface (ol_superset/cli.py) and metadata configuration (assets/metadata.yaml) have also seen recent changes. These changes suggest active development in reporting capabilities, cross-platform data migration, and infrastructure configuration, indicating these areas may be current pain points or undergoing significant enhancement.

## Evidence Summary

- Repository: `ol-data-platform`
- System type: dbt data transformation project
- Module graph nodes: `1106`
- Module graph edges: `902`
- Lineage datasets: `594`
- Lineage transformations: `589`
- Git analysis window: `90` days
- LLM-generated answers: `yes`

## Immediate Next Actions

1. Verify the top architectural hubs by navigating to their source files.
2. Validate upstream lineage for the highest-value sink datasets.
3. Inspect high-velocity files first — they're the most likely source of instability.
4. Review documentation drift flags before trusting any existing comments/docstrings.
5. Run `cartographer query <repo> --cartography-dir .cartography` to interactively explore.
