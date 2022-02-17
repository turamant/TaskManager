import os
import datetime

import asyncio
import subprocess

from dotenv import load_dotenv

from sqlalchemy.orm import Session

from models import engine, DoneTask, Task
from send_mailer import send_email


def done_task(task, cmd_time_end, cmd_out, cmd_err):
    """
    insert bd done_task
    """
    session = Session(bind=engine)
    donetask = DoneTask(
        command=task.command,
        date_on=task.date_on,
        date_off=cmd_time_end,
        text_out=cmd_out,
        text_err=cmd_err,
    )
    get_task = session.query(Task).get(task.id)
    get_task.task_done = True
    session.add(donetask)
    session.add(get_task)
    session.commit()


async def worker(name, work_queue):
    """
    worker tasks
    """
    while not work_queue.empty():
        print(f"Task {name} running!")
        task = await work_queue.get()

        with subprocess.Popen(task.command.split(),
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE) as cmd:
            cmd_out, cmd_err = cmd.communicate(password)

        cmd_out = cmd_out.decode('utf-8')
        cmd_err = cmd_err.decode('utf-8')
        cmd_time_end = datetime.datetime.now().replace(second=0, microsecond=0)
        done_task(task, cmd_time_end, cmd_out, cmd_err)
        print("The mail has been sent to e-mail")
        mail = 'Result: ' + cmd_out + '\nCommand errors: ' + cmd_err
        send_email(mail)
        print("Logger- Work completed: ", task.command)
        await asyncio.sleep(1)


async def main():
    """Task Queue"""
    session = Session(bind=engine)
    work_queue = asyncio.Queue()
    while True:
        q = session.query(Task)\
            .filter(Task.date_on == datetime.datetime.now().replace(second=0, microsecond=0))\
            .filter(Task.task_done == 'False')\
            .all()
        for work in q:
            work_queue.put_nowait(work)
        await asyncio.gather(asyncio.create_task(worker("-One-", work_queue)),
                             asyncio.create_task(worker("-Two-", work_queue))
                             )

def set_environ():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)


if __name__ == '__main__':
    set_environ()
    password = os.environ.get("SECRET_KEY").encode()
    asyncio.run(main())
