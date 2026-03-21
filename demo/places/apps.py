import os
import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class PlacesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'places'

    def ready(self):
        try:
            from pymongo import MongoClient
            client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017/'))
            db = client['geonames_demo']
            db.command('ping')
            logger.info("MongoDB connected successfully!")
        except Exception as e:
            logger.error(f"MongoDB connection error: {e}")
