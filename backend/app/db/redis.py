import redis.asyncio as redis

# Connect to your Redis instance (adjust host/port as needed)
# In production, you'd typically pull these from environment variables
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

async def add_jti_to_blocklist(jti: str) -> None:
    # Store the JTI as a key. The value can just be a placeholder (e.g., "1").
    # ex=3600 sets the Time-To-Live (TTL) to exactly 1 hour (3600 seconds).
    await redis_client.set(name=jti, value="1", ex=3600)

async def token_in_blocklist(jti: str) -> bool:
    # redis.exists() returns 1 if the key exists, 0 if it doesn't.
    # Redis automatically removes expired keys, so no manual cleanup is needed!
    exists = await redis_client.exists(jti)
    return bool(exists)