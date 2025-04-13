"""
Functions to calculate tree metrics from point cloud data.
"""

import logging
from typing import Dict, Optional
import numpy as np

import config
from src.preprocessing import get_points_at_height

logger = logging.getLogger(__name__)


def calculate_tree_height(tree_data: Dict[str, np.ndarray]) -> float:
    """
    Calculate the height of a tree from its point cloud data.

    Returns:
        Tree height in meters
    """
    z_cord = tree_data['xyz'][:, 2]

    min_z = np.min(z_cord)
    max_z = np.max(z_cord)

    height = max_z - min_z
    logger.info(f"Calculated tree height: {height:.3f}m")

    # pprint.pp(tree_data)
    return height


def calculate_dbh(tree_data: Dict[str, np.ndarray]) -> Optional[float]:
    """
    Calculate the Diameter at Breast Height (DBH) for a tree.

    Returns:
        DBH in meters, or None
    """
    try:
        trunk_mask = np.equal(tree_data['classification'], config.TRUNK_CLASS)

        if np.sum(trunk_mask) == 0:
            logger.warning("No trunk points found for DBH calculation")
            return None

        trunk_points = tree_data['xyz'][trunk_mask]

        dbh_slice = get_points_at_height(
            trunk_points,
            config.DBH_HEIGHT,
            config.DBH_TOLERANCE
        )

        if len(dbh_slice) < config.DBH_MIN_POINTS:
            logger.warning(f"Not enough points at breast height: {len(dbh_slice)} < {config.DBH_MIN_POINTS}")
            return None

        max_distance = 0.0

        for i in range(len(dbh_slice)):
            for j in range(i + 1, len(dbh_slice)):
                dx = dbh_slice[i, 0] - dbh_slice[j, 0]
                dy = dbh_slice[i, 1] - dbh_slice[j, 1]
                dist = np.sqrt(dx * dx + dy * dy)

                if dist > max_distance:
                    max_distance = float(dist)

        if max_distance > 0:
            logger.info(f"Calculated DBH: {max_distance:.3f}m")
            return float(max_distance)
        else:
            logger.warning("Could not determine DBH - no valid distances found")
            return None


    except Exception as e:
        logger.error(f"Error calculating DBH: {e}")
        return None


