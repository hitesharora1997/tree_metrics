"""
Functions to export tree metrics data.
"""

import pandas as pd
import config
import numpy as np
import logging
import os
import pyvista as pv
import matplotlib.pyplot as plt

from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def export_metrics_to_csv(metrics: Dict[int, Dict[str, float]], output_path: str) -> None:
    """
    Export tree metrics to a CSV file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    data = []
    for tree_id, tree_metrics in metrics.items():
        row = {'tree_id': tree_id}
        row.update(tree_metrics)
        data.append(row)

    df = pd.DataFrame(data)

    ordered_columns = ['tree_id', 'height', 'dbh']
    df = df[ordered_columns]

    df.to_csv(output_path, index=False)

    logger.info(f"Exported metrics for {len(metrics)} trees to {output_path}")

def create_metrics_summary(metrics: Dict[int, Dict[str, float]], output_dir: Optional[str] = None) -> Dict[str, Dict[str, float]]:
    """
    Create a summary of tree metrics with statistics.

    Returns:
        Dictionary with summary statistics
    """
    heights = [m['height'] for m in metrics.values() if 'height' in m and m['height'] is not None]
    dbhs = [m['dbh'] for m in metrics.values() if 'dbh' in m and m['dbh'] is not None]

    summary = {
        'height': {
            'count': len(heights),
            'min': min(heights) if heights else None,
            'max': max(heights) if heights else None,
            'mean': sum(heights) / len(heights) if heights else None,
            'std': np.std(heights) if heights else None
        },
        'dbh': {
            'count': len(dbhs),
            'min': min(dbhs) if dbhs else None,
            'max': max(dbhs) if dbhs else None,
            'mean': sum(dbhs) / len(dbhs) if dbhs else None,
            'std': np.std(dbhs) if dbhs else None
        }
    }

    logger.info("Tree metrics summary:")
    if heights:
        logger.info(f"Height (m): {len(heights)} trees, "
                   f"min={summary['height']['min']:.2f}, "
                   f"max={summary['height']['max']:.2f}, "
                   f"mean={summary['height']['mean']:.2f}, "
                   f"std={summary['height']['std']:.2f}")
    else:
        logger.info("Height (m): No valid height measurements")

    if dbhs:
        logger.info(f"DBH (m): {len(dbhs)} trees, "
                   f"min={summary['dbh']['min']:.2f}, "
                   f"max={summary['dbh']['max']:.2f}, "
                   f"mean={summary['dbh']['mean']:.2f}, "
                   f"std={summary['dbh']['std']:.2f}")
    else:
        logger.info("DBH (m): No valid DBH measurements")

    if output_dir and (heights or dbhs):
        create_metric_visualizations(metrics, output_dir)

    return summary


def visualize_with_pyvista(data: Dict[str, Any], color_by: str = 'tree_id') -> None:
    """
    Visualize the point cloud using PyVista as mentioned in the assignment.
    """
    if 'xyz' not in data:
        logger.error("Cannot visualize: No point cloud data provided")
        logger.info("For visualization, pass the original point cloud data, not the metrics")
        return

    try:
        xyz = data['xyz']

        cloud = pv.PolyData(xyz)

        if color_by == 'tree_id':
            cloud["point_color"] = data['tree_id']
            color_label = "Tree ID"
        elif color_by == 'classification':
            cloud["point_color"] = data['classification']
            color_label = "Classification"
        else:  # height (z-coordinate)
            cloud["point_color"] = xyz[:, 2]
            color_label = "Height (m)"

        logger.info(f"Visualizing point cloud colored by {color_label}...")
        p = pv.Plotter()
        p.add_points(
            cloud,
            render_points_as_spheres=True,
            point_size=config.POINT_SIZE,
            scalars='point_color',
            cmap=config.COLOR_MAP
        )
        p.add_scalar_bar(title=color_label)
        p.show()

    except ImportError:
        logger.warning("PyVista is not installed. Skipping 3D visualization.")
        logger.info("Install PyVista with: pip install pyvista")


def create_metric_visualizations(metrics: Dict[int, Dict[str, float]], output_dir: str) -> None:
    """
    Create visualizations of tree metrics (histograms, scatter plots).
    """
    os.makedirs(output_dir, exist_ok=True)

    tree_ids = list(metrics.keys())
    heights = [metrics[tid].get('height') for tid in tree_ids]
    dbhs = [metrics[tid].get('dbh') for tid in tree_ids]

    valid_data = [(tid, h, d) for tid, h, d in zip(tree_ids, heights, dbhs)
                  if h is not None and d is not None]

    if not valid_data:
        logger.warning("No valid data for visualization")
        return

    tree_ids_valid, heights_valid, dbhs_valid = zip(*valid_data)

    # 1. Height distribution histogram
    plt.figure(figsize=(10, 6))
    plt.hist(heights_valid, bins=10, edgecolor='black')
    plt.title('Tree Height Distribution')
    plt.xlabel('Height (m)')
    plt.ylabel('Number of Trees')
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(output_dir, 'height_distribution.png'), dpi=300)
    plt.close()

    # 2. DBH distribution histogram
    plt.figure(figsize=(10, 6))
    plt.hist(dbhs_valid, bins=10, edgecolor='black')
    plt.title('Tree DBH Distribution')
    plt.xlabel('DBH (m)')
    plt.ylabel('Number of Trees')
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(output_dir, 'dbh_distribution.png'), dpi=300)
    plt.close()

    # 3. Height vs DBH scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(dbhs_valid, heights_valid, alpha=0.7)
    plt.title('Tree Height vs DBH')
    plt.xlabel('DBH (m)')
    plt.ylabel('Height (m)')
    plt.grid(True, alpha=0.3)

    if len(valid_data) > 1:
        z = np.polyfit(dbhs_valid, heights_valid, 1)
        p = np.poly1d(z)
        plt.plot(sorted(dbhs_valid), p(sorted(dbhs_valid)), "r--", alpha=0.8)

    plt.savefig(os.path.join(output_dir, 'height_vs_dbh.png'), dpi=300)
    plt.close()

    logger.info(f"Created metric visualizations in {output_dir}")