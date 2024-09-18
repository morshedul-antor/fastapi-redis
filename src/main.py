from fastapi import FastAPI, Depends
from config import get_redis_pool
import aioredis
import uvicorn
import requests
import json

app = FastAPI(title="FastAPI Redis")


@app.get("/")
def root():
    return {"message": "FastAPI Redis Server!"}


@app.get("/comments")
async def get_items(redis: aioredis.Redis = Depends(get_redis_pool)):
    cache = await redis.get('comments')

    if cache:
        print("Cache hit...")
        return json.loads(cache)
    else:
        print("Cache missed..!")
        response = requests.get(
            'https://jsonplaceholder.typicode.com/comments')

        data = response.json()
        # cache clear after 10s
        await redis.setex('comments', 10, json.dumps(data))

        return data


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9000,
                reload=True, log_level="info")
