import redis
import os

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=6379,
    decode_responses=True
)
