import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN_DISK = os.getenv("TOKEN_DISK")
PATH_TO_SYNC_FOLDER = os.getenv("PATH_TO_SYNC_FOLDER")
PATH_TO_FOLDER_IN_DISK = os.getenv("PATH_TO_FOLDER_IN_DISK")
PERIOD_SYNC = int(os.getenv("PERIOD_SYNC"))
PATH_TO_LOG_FILE = os.getenv("PATH_TO_LOG_FILE")
