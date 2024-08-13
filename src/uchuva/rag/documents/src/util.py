#------------------------------------------
# Import necessary modules.
#------------------------------------------
import logging
import datetime
from pymongo import MongoClient

#------------------------------------------
# Define class.
#------------------------------------------
class MongoHandler(logging.Handler):
    """Custom logging handler for storing log entries in MongoDB."""

    def __init__(self, db):
        """Initializes the handler with a MongoDB Client."""
        super().__init__()
        self.db = db

    def emit(self, record):
        """Inserts the log entry into the MongoDB collection."""
        # Get time.
        current_date = datetime.datetime.now()
        # Define the logger.
        collection_name = f"{current_date.year}-{current_date.month}-{current_date.day}"
        collection = self.db[collection_name]
        log_entry = {
            'level': record.levelname,
            'filename': record.filename,
            'module': record.module,
            'lineno': record.lineno,
            'funcName': record.funcName,
            'message': self.format(record),
            'date': datetime.datetime.now(),
            'log_data': record.__dict__.get('log_data', {})
        }
        collection.insert_one(log_entry)

#------------------------------------------
# Define functions.
#------------------------------------------
def setup_mongo_logging(database_name, logger_name):
    """Sets up the logging to MongoDB."""
    # Define the logger.
    mongo_uri = "mongodb://192.168.0.22:27017"
    client = MongoClient(mongo_uri)
    db = client[database_name]
    mongo_handler = MongoHandler(db)
    logger = logging.getLogger(logger_name)
    logger.addHandler(mongo_handler)
    logger.setLevel(logging.INFO)
    return logger