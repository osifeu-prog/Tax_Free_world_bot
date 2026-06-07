# -*- coding: utf-8 -*-
import os, json
try:
    import redis.asyncio as redis
    r = redis.from_url(os.environ.get("REDIS_URL","redis://localhost:6379"), decode_responses=True)
except:
    r = None
async def cache_get(k): return await r.get(k) if r else None
async def cache_set(k,v,ttl=3600):
    if r: await r.setex(k,ttl,v)

