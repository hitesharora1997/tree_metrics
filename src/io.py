"""
I/O functions for working with LiDAR data in LAS format.
"""
import logging
import numpy as np
import laspy
from typing import Dict, Any


logger = logging.getLogger(__name__)

def read_las_file(file_path: str) -> Dict[str, Any]:
    """
    Read lidar files (.las) and extract data

    Returns:
        Dictionary containing extracted data:
        - 'xyz': Point coordinates as numpy array (n, 3)
        - 'classification': Point classifications
        - 'tree_id': Tree IDs for each point
        - 'header': LAS file header information
        - 'point_count': Number of points in the file
    """
    logger.info(f"Reading las file: {file_path}")

    try:
        with laspy.open(file_path) as fh:
            header = fh.header
            p_count = header.point_count
            print(p_count)

            logger.info(f"Found {p_count} points in the las file")

            points = fh.read()

            xyz = np.column_stack([points.x, points.y, points.z])

            classification = points.classification

            available_attrs = [attr for attr in dir(points) if not attr.startswith('_')]
            logger.debug(f"Available point attributes: {available_attrs}")

            trees_id = None
            tree_id_fields = ["treeID", "tree_id", "TreeID", "tree_ID", "user_data", "point_source_id"]

            for field in tree_id_fields:
                if hasattr(points, field):
                    trees_id = getattr(points, field)
                    logger.info(f"Found tree ID data in field: {field}")
                    break

        data = {
            'xyz': xyz,
            'classification': classification,
            'tree_id': trees_id,
            'header': header,
            'point_count': p_count
        }

        logger.info(f"Point cloud bounds: "
                    f"X({min(xyz[:, 0]):.2f} to {max(xyz[:, 0]):.2f}), "
                    f"Y({min(xyz[:, 1]):.2f} to {max(xyz[:, 1]):.2f}), "
                    f"Z({min(xyz[:, 2]):.2f} to {max(xyz[:, 2]):.2f})")

        unique_classes = np.unique(classification)
        logger.info(f"Classification values: {unique_classes}")

        unique_tree_id = np.unique(trees_id)
        logger.info(f"Found unique tree {len(unique_tree_id)}")

        return data

    except Exception as e:
        logger.error(f"Error reading LAS file: {e}")
        raise
