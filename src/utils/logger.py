import logging
import logging.handlers
from pathlib import Path


def setup_logger(
    name: str = "portfolio",
    log_file: str = "logs/portfolio.log",
    level: str = "INFO"
) -> logging.Logger:
    """
    Setup application logger with file and console handlers
    
    Args:
        name: Logger name
        log_file: Path to log file
        level: Logging level
        
    Returns:
        Configured logger
    """
    pass
