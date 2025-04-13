"""
Tests for preprocessing functions.
"""
import numpy as np
from src.preprocessing import group_points_by_trees, get_points_at_height
import config


class TestPreprocessing:
    def test_group_points_by_trees(self):
        """Test grouping points by tree ID."""
        data = {
            'xyz': np.array([
                [0, 0, 0],  # Tree 1
                [1, 1, 1],  # Tree 1
                [2, 2, 2],  # Tree 2
                [3, 3, 3],  # Tree 2
                [4, 4, 4],  # Ground
            ]),
            'classification': np.array([1, 2, 1, 3, 0]),
            'tree_id': np.array([1, 1, 2, 2, 0])
        }

        result = group_points_by_trees(data)

        # Assertions
        assert len(result) == 2
        assert 1 in result
        assert 2 in result
        assert len(result[1]['xyz']) == 2
        assert len(result[2]['xyz']) == 2


def test_get_points_at_height():
    """Test extracting points at a specific height."""
    points = np.array([
        [0, 0, 1.0],
        [1, 1, 1.25],
        [2, 2, 1.3],
        [3, 3, 1.35],
        [4, 4, 1.4],
    ])

    result = get_points_at_height(points, config.DBH_HEIGHT, 0.05)

    assert len(result) == 3
    assert np.array_equal(result[0], np.array([1, 1, 1.25]))
    assert np.array_equal(result[1], np.array([2, 2, 1.3]))
    assert np.array_equal(result[2], np.array([3, 3, 1.35]))