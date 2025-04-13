"""
Processing pipeline for LiDAR point cloud data.
"""

import logging
from typing import Dict, Any
from .preprocessing import group_points_by_trees
from .metrics import calculate_tree_height, calculate_dbh

logger = logging.getLogger(__name__)

def process_point_cloud(data: Dict[str, Any]) -> Dict[int, Dict[str, float]]:
    """
    Process tje point data to calculate tree metrics

    Returns:
        Dictionary with tree metrics (height, dbh) for each tree ID
    """

    logger.info("Grouping points by tree ID")
    trees = group_points_by_trees(data)
    logger.info(f"Processing {len(trees)} trees")

    metrics = {}
    for tree_id, tree_data in trees.items():
        logger.info(f"Processing tree {tree_id}")

        # Height Calculation
        try:
            height = calculate_tree_height(tree_data)
            logger.info(f"Tree {tree_id} height: {height:.3f}m")
        except Exception as e:
            logger.error(f"Error calculating height for tree {tree_id}: {e}")
            height = None

        # DBH Calculation
        try:
            dbh = calculate_dbh(tree_data)
            logger.info(f"Tree {tree_id} DBH: {dbh:.3f}m")
        except Exception as e:
            logger.error(f"Error calculating DBH for tree {tree_id}: {e}")
            dbh = None

        metrics[tree_id] = {
            'height': height,
            'dbh': dbh
        }

    return metrics




