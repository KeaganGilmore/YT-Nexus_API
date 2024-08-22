import os

class Config:
    EXTERNAL_API_BASE_URL = 'https://lxlibrary.online/yt-nexus'
    REQUEST_TIMEOUT = 10
    MAX_WORKERS = 5
    DEBUG = True
    LOG_FILE = os.path.join('logs', 'app.log')
