"""
Tests for the exporter functions.
"""
import os
import pandas as pd
from src.exporter import export_metrics_to_csv


def test_export_metrics_to_csv(tmp_path):
    """Test exporting metrics to CSV file."""
    # Create mock metrics
    metrics = {
        1: {'height': 10.5, 'dbh': 0.35},
        2: {'height': 15.2, 'dbh': 0.42}
    }

    output_path = tmp_path / "test_metrics.csv"

    export_metrics_to_csv(metrics, output_path)

    assert os.path.exists(output_path)

    df = pd.read_csv(output_path)
    assert list(df.columns) == ['tree_id', 'height', 'dbh']
    assert len(df) == 2

    tree1 = df[df['tree_id'] == 1].iloc[0]
    assert tree1['height'] == 10.5
    assert tree1['dbh'] == 0.35