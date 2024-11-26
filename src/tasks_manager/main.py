import asyncio
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from manager import TasksManager, logger


async def main():
    tasks_manager = TasksManager(
        os.getenv("RABBITMQ_SERVER"),
        os.getenv("RABBITMQ_PORT"),
        os.getenv("RABBITMQ_USER"),
        os.getenv("RABBITMQ_PASSWORD"),
    )

    await tasks_manager.initialize()

    await tasks_manager.update_hashtags_to_monitor()
    await tasks_manager.send_tasks_to_queue()

    scheduler = AsyncIOScheduler()

    # update hashtags to monitor every 30 minutes
    scheduler.add_job(tasks_manager.update_hashtags_to_monitor, "interval", minutes=30)

    # send tasks to queue at 10:00 and 16:00
    scheduler.add_job(tasks_manager.send_tasks_to_queue, "cron", hour=0, minute=1)
    scheduler.add_job(tasks_manager.send_tasks_to_queue, "cron", hour=8, minute=1)
    scheduler.add_job(tasks_manager.send_tasks_to_queue, "cron", hour=16, minute=1)

    scheduler.start()

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    logger.info("Tasks Manager started")
    asyncio.run(main())
    logger.info("Tasks Manager stopped")
