import logging

logging.basicConfig(filename="system.log", level=logging.INFO)

try
    raise ValueError("Example failure")
except Exception as e:
    logging.error(f"Error occurred: {e}")
