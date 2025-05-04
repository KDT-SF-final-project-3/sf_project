
# auto_drive/apps.py

from django.apps import AppConfig
import threading
from .detector_thread import run_detector

class AutoDriveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auto_drive'

    def ready(self):
        t = threading.Thread(target=run_detector, daemon=True)
        t.start()