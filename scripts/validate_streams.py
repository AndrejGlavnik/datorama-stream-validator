from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from datorama_stream_validator.validator import load_rules, render_markdown, validate_streams


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Datorama-style stream naming rules.")
    parser.add_argument("--input", required=True, help="CSV stream inventory.")
    parser.add_argument("--rules", default="config/naming_rules.yml", help="YAML naming rules.")
    parser.add_argument("--out", default="reports/stream_validation_report.md", help="Markdown output path.")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    rules = load_rules(args.rules)
    results = validate_streams(df, rules)
    report = render_markdown(results, Path(args.input).name)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(f"Wrote {out} with {len(results)} rule group(s).")


if __name__ == "__main__":
    main()
