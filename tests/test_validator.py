import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from datorama_stream_validator.validator import load_rules, validate_streams


def test_sample_stream_inventory_flags_taxonomy_and_pattern_issues():
    df = pd.read_csv(ROOT / "sample_data" / "data_streams.csv")
    rules = load_rules(ROOT / "config" / "naming_rules.yml")
    result_rules = {result.rule for result in validate_streams(df, rules)}
    assert "stream_name_pattern" in result_rules
    assert "campaign_name_pattern" in result_rules
    assert "country_taxonomy" in result_rules
    assert "source_taxonomy" in result_rules
