import redis
import os

from dotenv import load_dotenv

load_dotenv()

print(os.getenv("REDIS_HOST"))
# Redis connection setup
redis_client = redis.StrictRedis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=0)

def store_token_in_redis(token_data,REDIS_TOKEN_KEY):
    """Store token data in Redis."""
    redis_client.set(REDIS_TOKEN_KEY, token_data)

def retrieve_token_from_redis(REDIS_TOKEN_KEY):
    """Retrieve token data from Redis."""
    token_data = redis_client.get(REDIS_TOKEN_KEY)
    if token_data:
        return token_data.decode('utf-8')
    return None