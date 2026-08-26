import os

class Config:
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_DATA_PORT = int(os.getenv('REDIS_DATA_PORT', 6379))
    REDIS_SEARCH_PORT = int(os.getenv('REDIS_SEARCH_PORT', 6380))
    INDEX_NAME = os.getenv('REDIS_INDEX_NAME', 'my_index')
