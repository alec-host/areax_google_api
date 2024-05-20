import redis

# Redis connection setup
redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

REDIS_TOKEN_KEY = 'gmail_token'

def store_token_in_redis(token_data):
    """Store token data in Redis."""
    redis_client.set(REDIS_TOKEN_KEY, token_data)

def retrieve_token_from_redis():
    """Retrieve token data from Redis."""
    token_data = redis_client.get(REDIS_TOKEN_KEY)
    if token_data:
        return token_data.decode('utf-8')
    return None