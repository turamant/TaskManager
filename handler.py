import os
import datetime

import subprocess
from queue import Queue

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


def worker(name, work_queue):
    """
    worker tasks
    """
    while not work_queue.empty():
        task = work_queue.get()
        password = os.environ.get("SECRET_KEY").encode()
        with subprocess.Popen(task.command.split(),
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE) as cmd:
            cmd_out, cmd_err = cmd.communicate(password)

        cmd_out = cmd_out.decode('utf-8')
        cmd_err = cmd_err.decode('utf-8')
        cmd_time_end = datetime.datetime.now().replace(second=0, microsecond=0)
        done_task(task, cmd_time_end, cmd_out, cmd_err)
        mail = f'Result: {cmd_out} \nCommand errors: {cmd_err}'
        send_email(mail)


def main():
    """Task Queue"""
    session = Session(bind=engine)
    work_queue = Queue()
    while True:
        q = session.query(Task)\
            .filter(Task.date_on == datetime.datetime.now()
                    .replace(second=0, microsecond=0))\
            .filter(Task.task_done == 'False')\
            .all()
        for work in q:
            work_queue.put_nowait(work)
        worker("-One-", work_queue)


def set_dotenviromment():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    else:
        print('Файл .env отсутствует!')
        exit()


if __name__ == '__main__':
    set_dotenviromment()
    main()
