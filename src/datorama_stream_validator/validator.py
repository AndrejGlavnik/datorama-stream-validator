from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import yaml


@dataclass
class RuleResult:
    rule: str
    severity: str
    failures: int
    message: str
    next_action: str


def load_rules(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def validate_streams(df: pd.DataFrame, rules: dict[str, Any]) -> list[RuleResult]:
    results: list[RuleResult] = []
    required_missing = [field for field in rules["required_fields"] if field not in df.columns]
    if required_missing:
        results.append(
            RuleResult(
                "required_fields",
                "high",
                len(required_missing),
                "Missing required field(s): " + ", ".join(required_missing),
                "Update the stream inventory export or validator config before QA can continue.",
            )
        )
        return results

    stream_pattern = re.compile(rules["stream_name_pattern"])
    campaign_pattern = re.compile(rules["campaign_pattern"])

    invalid_streams = int((~df["stream_name"].astype(str).str.match(stream_pattern)).sum())
    if invalid_streams:
        results.append(
            RuleResult(
                "stream_name_pattern",
                "high",
                invalid_streams,
                f"{invalid_streams} stream name(s) do not match the approved pattern.",
                "Rename streams or document an approved exception before dashboard refresh.",
            )
        )

    invalid_campaigns = int((~df["campaign_name"].astype(str).str.match(campaign_pattern)).sum())
    if invalid_campaigns:
        results.append(
            RuleResult(
                "campaign_name_pattern",
                "medium",
                invalid_campaigns,
                f"{invalid_campaigns} campaign name(s) do not match the approved pattern.",
                "Ask media owners to normalize campaign names or update taxonomy rules.",
            )
        )

    for field, allowed_key in [
        ("country", "allowed_countries"),
        ("category", "allowed_categories"),
        ("source", "allowed_sources"),
    ]:
        invalid = int((~df[field].isin(rules[allowed_key])).sum())
        if invalid:
            results.append(
                RuleResult(
                    f"{field}_taxonomy",
                    "high" if field in {"country", "source"} else "medium",
                    invalid,
                    f"{invalid} row(s) contain {field} values outside the approved list.",
                    f"Correct {field} values or add approved exceptions to the governance rules.",
                )
            )

    return results


def render_markdown(results: list[RuleResult], input_name: str) -> str:
    lines = [
        "# Datorama Stream Validation Report",
        "",
        f"Input file: `{input_name}`",
        "",
        f"Summary: {len(results)} rule group(s) need review.",
        "",
        "| Rule | Severity | Failures | Finding | Next action |",
        "|---|---:|---:|---|---|",
    ]
    for result in results:
        lines.append(
            f"| {result.rule} | {result.severity} | {result.failures} | {result.message} | {result.next_action} |"
        )
    lines.extend(
        [
            "",
            "## Why this matters",
            "",
            "Consistent stream and campaign naming keeps dashboard filters, ownership, data joins and stakeholder reporting logic maintainable.",
        ]
    )
    return "\n".join(lines) + "\n"
