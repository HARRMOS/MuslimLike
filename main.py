from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import aiomysql

app = FastAPI()

class LikeRequest(BaseModel):
    userId: int

# Config de ta base de données
DB_CONFIG = {
    "host": "mh285989-001.eu.clouddb.ovh.net",
    "port": 35693,
    "user": "bts",
    "password": "Harris91270",
    "db": "MuslimVibe",
}

# Connexion pool
@app.on_event("startup")
async def startup():
    app.state.pool = await aiomysql.create_pool(**DB_CONFIG)

@app.on_event("shutdown")
async def shutdown():
    app.state.pool.close()
    await app.state.pool.wait_closed()

# Endpoint pour liker / déliker
@app.post("/content/{content_id}/like")
async def toggle_like(content_id: int, request: LikeRequest):
    async with app.state.pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT EXISTS(SELECT 1 FROM likes WHERE user_id = %s AND content_id = %s)",
                (request.userId, content_id)
            )
            (has_liked,) = await cur.fetchone()

            if has_liked:
                await cur.execute(
                    "DELETE FROM likes WHERE user_id = %s AND content_id = %s",
                    (request.userId, content_id)
                )
                await conn.commit()
                return {"liked": False}
            else:
                await cur.execute(
                    "INSERT INTO likes (user_id, content_id) VALUES (%s, %s)",
                    (request.userId, content_id)
                )
                await conn.commit()
                return {"liked": True}

# Endpoint pour obtenir le nombre de likes
@app.get("/content/{content_id}/likes")
async def get_likes(content_id: int):
    async with app.state.pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT COUNT(*) FROM likes WHERE content_id = %s",
                (content_id,)
            )
            (count,) = await cur.fetchone()
            return {"count": count}
