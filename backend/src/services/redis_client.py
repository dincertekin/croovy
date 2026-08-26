import redis
from config import Config

redis_data_client = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_DATA_PORT,
    decode_responses=True
)

redis_search_client = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_SEARCH_PORT,
    decode_responses=True
)
