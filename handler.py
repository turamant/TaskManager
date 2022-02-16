import asyncio
import datetime

from sqlalchemy.orm import Session

from models import engine, DoneTask, Task

async def main():
    session = Session(bind=engine)
    work_queue = asyncio.Queue()
    while True:
        q = session.query(Task).\
            filter(Task.date_on == datetime.datetime.now()
                   .replace(second=0, microsecond=0))\
            .filter(Task.task_done == 'False').all()
        for work in q:
            work_queue.put_nowait(work)

        await asyncio.gather(asyncio.create_task(worker("-One-", work_queue)),
                             asyncio.create_task(worker("-Two-", work_queue))
                             )