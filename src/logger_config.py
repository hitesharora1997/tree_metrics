import logging
import os
from typing import Optional


def setup_logging(log_file: Optional[str] ='tree_metrics.log', log_level: str ='INFO'):
    """
    Configure the application's logging system.
    """

    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Console output
            logging.FileHandler(log_file)  # File output
        ]
    )


    logger = logging.getLogger(__name__)
    logger.debug(f"Logging configured: level={log_level}, file={log_file}")