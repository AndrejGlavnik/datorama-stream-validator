# Datorama Stream Validation Report

Input file: `data_streams.csv`

Summary: 4 rule group(s) need review.

| Rule | Severity | Failures | Finding | Next action |
|---|---:|---:|---|---|
| stream_name_pattern | high | 2 | 2 stream name(s) do not match the approved pattern. | Rename streams or document an approved exception before dashboard refresh. |
| campaign_name_pattern | medium | 1 | 1 campaign name(s) do not match the approved pattern. | Ask media owners to normalize campaign names or update taxonomy rules. |
| country_taxonomy | high | 1 | 1 row(s) contain country values outside the approved list. | Correct country values or add approved exceptions to the governance rules. |
| source_taxonomy | high | 1 | 1 row(s) contain source values outside the approved list. | Correct source values or add approved exceptions to the governance rules. |

## Why this matters

Consistent stream and campaign naming keeps dashboard filters, ownership, data joins and stakeholder reporting logic maintainable.
