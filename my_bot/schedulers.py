import asyncio

import aioschedule


async def schedule_jobs():
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(3600)  # 1 час
