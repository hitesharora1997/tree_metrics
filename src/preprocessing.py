"""
Preprocessing functions for LiDAR point cloud data.
"""

import numpy as np
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def group_points_by_trees(data: Dict[str,Any]) -> Dict[int, Dict[str, np.ndarray]]:
    """
    Group points by tree ID.

    Returns:
       Dictionary with tree IDs as keys, and for each tree ID, a dictionary with:
       - 'xyz': Points belonging to this tree
       - 'classification': Classifications of these points
   """
    xyz = data['xyz']
    classification = data['classification']
    tree_id = data['tree_id']

    unique_tree_ids = np.unique(tree_id)
    unique_tree_ids = unique_tree_ids[unique_tree_ids > 0]

    logger.info(f"Found {len(unique_tree_ids)} unique trees in the point cloud")

    trees = {}
    for tid in unique_tree_ids:
        tree_mask = tree_id == tid

        tree_xyz = xyz[tree_mask]
        tree_classification = classification[tree_mask]

        trees[int(tid)] = {
            'xyz': tree_xyz,
            'classification': tree_classification
        }

        logger.debug(f"Tree {tid}: {len(tree_xyz)} points")
    return trees

def get_points_at_height(
        points: np.ndarray,
        target_height: float,
        tolerance: float = 0.05 ) -> np.ndarray:
    """
    Extract points within a specific height range.

    Returns:
       Array of points within the specified height range
    """
    height_mask = (points[:, 2] >= target_height - tolerance) & (points[:, 2] <= target_height + tolerance)
    return points[height_mask]