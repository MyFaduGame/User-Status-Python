#FastAPI Imports
from fastapi import FastAPI,Request,status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json

#Local Imports
from redis_conn import (
    set_to_redis,
    get_from_redis,
    get_list_user
)

app = FastAPI(
    title="Fantasy Cult",
    description="Fantasy Cult",
    version="1",
)
# @app.on_event("startup")
# async def startup():
#     await db.create_all()
# @app.on_event("shutdown")
# async def shutdown():
#     await db.close()
    
    
user_list = [
    {
        'username':"random0",
        "user":"offline"
    },
    {
        'username':"random1",
        "user":"offline"
    },
    {
        'username':"random2",
        "user":"online"
    },
    {
        'username':"random3",
        "user":"offline"
    },
    {
        'username':"random4",
        "user":"offline"
    },
    {
        'username':"random5",
        "user":"online"
    },
    {
        'username':"random6",
        "user":"online"
    },
]
    
@app.get('/user')
async def set_users():
    for i in user_list:
        await set_to_redis(
            key_name=i['username'],
            value_name=json.dumps(i),
            expire=3600
        )
    return True
            

@app.post('/{username}/{on_off}')
async def request_response(username:str,on_off:bool):
    data = await get_from_redis(
        key_name=username
    )
    data = json.loads(data)
    if on_off:
        data['user']='online'
    else:
        data['user'] = 'offline'
    await set_to_redis(
        key_name=username,
        value_name=json.dumps(data)
    )
    return {
        'status_code':status.HTTP_200_OK,
        'data':data
    }

@app.get('/')
async def response_struc():
    data = await get_list_user(
        key_name='random'
    )
    if data:
        return {
            'status_code':status.HTTP_200_OK,
            'data':data
        }
    else:
        return {
            'status_code':status.HTTP_200_OK,
            'data':[]
        }

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)