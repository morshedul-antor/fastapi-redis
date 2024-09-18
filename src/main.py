from utils import get_redis_cache, set_redis_cache
from fastapi import FastAPI, Depends
from config import get_redis_pool
import aioredis
import uvicorn
import requests
import json

app = FastAPI(title="FastAPI Redis")


@app.get("/")
def root():
    return {"message": "FastAPI Redis!"}


@app.get("/comments")
async def get_items(redis: aioredis.Redis = Depends(get_redis_pool)):
    cache = await get_redis_cache(redis, "comments")

    if cache:
        print("Cache hit...")
        return cache
    else:
        print("Cache missed..!")
        response = requests.get(
            'https://jsonplaceholder.typicode.com/comments')

        data = response.json()
        # Cache clear after 10s
        await set_redis_cache(redis, "comments", data, 10)

        return data


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8050,
                reload=True, log_level="info")
