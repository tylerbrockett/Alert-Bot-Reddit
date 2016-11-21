from utils.database import DB_FILE_NAME
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_LOCATION = os.path.join(ROOT_DIR, 'database', DB_FILE_NAME)
