"""
Tests for the I/O functions.
"""
import numpy as np
from unittest.mock import patch, MagicMock
from src.io import read_las_file


def test_read_las_file_mock():
    """Test reading LAS file using mocks."""
    x = np.array([1, 2, 3, 4] * 25)
    y = np.array([5, 6, 7, 8] * 25)
    z = np.array([9, 10, 11, 12] * 25)
    classification = np.array([0, 1, 2, 3] * 25)
    tree_id = np.array([0, 1, 2, 3] * 25)

    with patch('laspy.open') as mock_open:
        mock_context = MagicMock()
        mock_open.return_value = mock_context

        mock_file = MagicMock()
        mock_context.__enter__.return_value = mock_file

        mock_file.header = MagicMock()
        mock_file.header.point_count = 100

        mock_points = MagicMock()
        mock_points.x = x
        mock_points.y = y
        mock_points.z = z
        mock_points.classification = classification
        mock_points.treeID = tree_id
        mock_file.read.return_value = mock_points

        with patch('numpy.min', return_value=0), patch('numpy.max', return_value=10):
            result = read_las_file('fake_file.las')

    assert 'xyz' in result
    assert 'classification' in result
    assert 'tree_id' in result
    assert result['point_count'] == 100
    assert result['xyz'].shape == (100, 3)