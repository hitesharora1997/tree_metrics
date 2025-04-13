"""
Tests for the point cloud processing pipeline.
"""
import config
import numpy as np
from src.processor import process_point_cloud


def test_process_point_cloud():
    """Test the complete point cloud processing pipeline."""
    data = {
        'xyz': np.array([
            [0, 0, 0],
            [0.1, 0, 1.3],
            [-0.1, 0, 1.3],
            [0, 0.1, 1.3],
            [0, -0.1, 1.3],
            [0, 0, 10],
        ]),
        'classification': np.array([1, 1, 1, 1, 1, 3]),
        'tree_id': np.array([1, 1, 1, 1, 1, 1])
    }

    original_min_points = config.DBH_MIN_POINTS
    config.DBH_MIN_POINTS = 4

    try:
        metrics = process_point_cloud(data)

        assert 1 in metrics
        assert 'height' in metrics[1]
        assert 'dbh' in metrics[1]
        assert metrics[1]['height'] == 10.0
        assert 0.18 <= metrics[1]['dbh'] <= 0.22
    finally:
        config.DBH_MIN_POINTS = original_min_points