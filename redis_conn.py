#Third Party Imports
import redis,json
from fastapi import status
from pydantic import constr
from fastapi.exceptions import HTTPException

#Local Imports

REDIS_URL = '127.0.0.1'
REDIS_PORT = 6379

# redis_connection = redis.from_url(
#     url='redis://localhost:8000/0'
# )

try:
    redis_connection = redis.Redis(
        host=REDIS_URL,
        port=REDIS_PORT,
        db=0
    )
except Exception as e:
    raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,detail="Redis Connection Failed")
    


async def set_to_redis(key_name:constr(),value_name,expire:int=60):
    try:
        redis_connection.set(
            name=key_name,
            value=value_name,
            ex=expire
        )
        return True
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,detail="Redis Connection Failed")
        


async def get_from_redis(key_name:constr()):
    try:
        data = redis_connection.get(
            name=key_name,
        )
        if data:
            return data
        else:
            return None
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,detail="Redis Connection Failed")
        
async def get_list_user(key_name:constr()):
    try:
        data = redis_connection.scan_iter(f'{key_name}*')
        user_data = []
        if data:
            for i in data:
                new_data = await get_from_redis(
                    key_name=i.decode()
                )
                user_data.append(json.loads(new_data))
            return user_data
        else:
            return None
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,detail="Redis Connection Failed") 