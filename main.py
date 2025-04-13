"""
Driver program for processing LiDAR point cloud data to extract tree metrics.
"""
import argparse
import logging
import sys
import  config
import os

from src.logger_config import setup_logging
from src.io import read_las_file
from src.exporter import export_metrics_to_csv
from src.processor import process_point_cloud
from src.exporter import visualize_with_pyvista, create_metrics_summary

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process Lidar point cloud data to extract tree metrics")
    parser.add_argument("input_file", help="Path to the input LAS file")
    parser.add_argument("--output", "-o", default=config.DEFAULT_OUTPUT_FILE,
                        help="Path to the output CSV file")
    parser.add_argument("--visualize", "-v", action="store_true",
                        help="Create visualization plots")
    parser.add_argument("--log-level", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='INFO',
                        help="Set the logging level")
    parser.add_argument("--log-file", default="logs/tree_metrics.log",
                        help="Path to the log file")
    parser.add_argument("--visualize-3d", action="store_true",
                        help="Visualize the point cloud in 3D using PyVista")
    parser.add_argument("--color-by", choices=['tree_id', 'classification', 'height'],
                        default='tree_id', help="Color points by this attribute")

    return parser.parse_args()

def main():
    """
    Driver function to process the point cloud data
    """
    args = parse_arguments()

    setup_logging(args.log_file, args.log_level)

    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Loading the point cloud from {args.input_file}")
        data = read_las_file(args.input_file)

        metrics = process_point_cloud(data)

        export_metrics_to_csv(metrics, args.output)
        logger.info(f"Metrics exported to {args.output}")

        if args.visualize:
            output_dir = os.path.dirname(args.output)
            create_metrics_summary(metrics, output_dir)

        if args.visualize_3d:
            visualize_with_pyvista(data, args.color_by)

        logger.info("Processing completed successfully")
        return 0

    except Exception as e:
        logger.error(f"Error processing the cloud points: {e}", exc_info=True)
        return 1



if __name__ == "__main__":
    sys.exit(main())