"""
==========================================
Author:             Tyler Brockett
Username:           /u/tylerbrockett
Description:        Alert Bot (Formerly sales__bot)
Date Created:       11/13/2015
Date Last Edited:   11/28/2016
Version:            v2.0
==========================================
"""

from utils.database import DB_FILE_NAME
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_LOCATION = os.path.join(ROOT_DIR, 'database', DB_FILE_NAME)
