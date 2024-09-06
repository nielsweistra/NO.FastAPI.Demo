# /base/logger/logger.py
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# ANSI escape codes for coloring
RESET = "\033[0m"  # Reset color
GREEN = "\033[32m"  # Green color for INFO level

class CustomFormatter(logging.Formatter):
    FORMATS = {
        logging.INFO: f"{GREEN}%(levelname)s:{RESET}     %(asctime)s - %(message)s{RESET}",
        'default': "%(levelname)s:     %(asctime)s - %(message)s"
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.FORMATS['default'])
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# Define log file path
log_file_path = Path(__file__).parent / "app.log"

# Define the maximum file size (e.g., 5 MB) and backup count
max_file_size = 5 * 1024 * 1024  # 5 MB
backup_count = 3

# Create and configure the logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)  # Set the default logging level

# Create handlers
console_handler = logging.StreamHandler()  # Output logs to the console
file_handler = RotatingFileHandler(log_file_path, maxBytes=max_file_size, backupCount=backup_count)  # Output logs to a file with rotation

# Set logging level for each handler
console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.INFO)

# Use custom formatter for console to apply colors, plain format for file
console_handler.setFormatter(CustomFormatter())
file_handler.setFormatter(logging.Formatter(CustomFormatter.FORMATS['default']))

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
