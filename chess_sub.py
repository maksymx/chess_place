import asyncio
import ujson
from pprint import pprint

import aioredis


async def chess_read(channel):
    while True:
        msg = await channel.get(encoding='utf-8')
        if not msg:
            break
        pprint(ujson.loads(msg))


async def chess_sub():
    pool = await aioredis.create_pool(('localhost', 6379))
    async with pool.get() as redis:
        channel, = await redis.subscribe("team_chess:1")
        print("Client has been subscribed to channel team_chess:1")

        await chess_read(channel)

        await redis.unsubscribe("team_chess:1")
        print("Client has been unsubscribed from channel team_chess:1")
        # value = await conn.get('my-key')
        # print('raw value:', value)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(chess_sub())
