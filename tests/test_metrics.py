"""
Tests for tree metrics calculations.
"""
import numpy as np
from src.metrics import calculate_tree_height, calculate_dbh
import config

class TestMetrics:
    def test_calculate_tree_height(self):
        tree_data = {
            'xyz': np.array([
                [0, 0, 0],   # Base of tree
                [0, 0, 5],   # Mid tree
                [0, 0, 10],  # Top of tree
            ]),
            'classification': np.array([1, 1, 3])
        }

        height = calculate_tree_height(tree_data)

        assert height == 10.0

    def test_calculate_dbh(self):
        """Test DBH calculation with sufficient points at breast height."""
        theta = np.linspace(0, 2*np.pi, 8)
        radius = 0.2

        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        z = np.full_like(theta, config.DBH_HEIGHT)

        tree_data = {
            'xyz': np.column_stack([x, y, z]),
            'classification': np.full(len(theta), config.TRUNK_CLASS)
        }

        dbh = calculate_dbh(tree_data)

        assert dbh is not None
        assert 0.38 <= dbh <= 0.42

    def test_calculate_dbh_insufficient_points(self):
        """Test DBH calculation with insufficient points."""
        tree_data = {
            'xyz': np.array([
                [0, 0, 0],
                [0, 0, 5],
            ]),
            'classification': np.array([config.TRUNK_CLASS, config.TRUNK_CLASS])
        }

        dbh = calculate_dbh(tree_data)

        assert dbh is None