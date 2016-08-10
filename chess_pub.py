import asyncio
import ujson

import aioredis

from chess_place import ChessPlace


async def chess_pub():
    pool = await aioredis.create_pool(('localhost', 6379))
    cp = ChessPlace(['knight', 'pawn', 'king'])
    desk = cp.place_pieces()
    async with pool.get() as redis:
        redis.publish("team_chess:1", ujson.dumps(desk))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(chess_pub())
