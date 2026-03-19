import os
import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class LaureatesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'laureates'

    def ready(self):
        import sys
        if not os.environ.get('RUN_MAIN') and ('runserver' in sys.argv):
            try:
                from pymongo import MongoClient
                from .tools.db_init import create_indexes
                client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017/'))
                db = client['nobel_demo']
                db.command('ping')
                logger.info("MongoDB connected successfully!")
                create_indexes(db)
            except Exception as e:
                logger.error(f"MongoDB connection error: {e}")
