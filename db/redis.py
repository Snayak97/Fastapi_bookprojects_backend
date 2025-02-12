from redis.asyncio import Redis

from config import Config
JWT_ID_EXPIRY= 3600

token_blocklist = Redis(
    host = Config.REDIS_HOST,
    port = Config.REDIS_PORT,
    db= 0
)

async def add_jwt_id_to_blocklist(jwt_id:str)->None:
    await token_blocklist.set(name = jwt_id, value="", ex = JWT_ID_EXPIRY)

async def token_in_blocklist(jwt_id:str)->None:
    jwt_id= await token_blocklist.get(jwt_id)
    return jwt_id is not None
