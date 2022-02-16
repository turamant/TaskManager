import asyncio
import datetime
import os
import subprocess
import sys
from configparser import ConfigParser

from sqlalchemy.orm import Session

from models import engine, DoneTask, Task
from send_mailer import send_email


def parse_config():
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "conf.ini")
    if os.path.exists(config_path):
        cfg = ConfigParser()
        cfg.read(config_path)
        password = cfg.get("passw", "password")
        return password
    else:
        print("Config not found! Exiting!")
        sys.exit(1)


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
    worker
    """
    while not work_queue.empty():
        print(f"задание {name} запущено!")
        task = await work_queue.get()

        with subprocess.Popen(task.command.split(),
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE) as cmd:
            cmd_out, cmd_err = cmd.communicate(password)

        cmd_out = cmd_out.decode('utf-8')
        cmd_err = cmd_err.decode('utf-8')

        if cmd_err == b'':
            cmd_time_end = datetime.datetime.now()\
                .replace(second=0, microsecond=0)
            done_task(task, cmd_time_end, cmd_out, cmd_err)
            print("Почта отправлена на e-mail")
            mail = 'Результат испонения комманды: ' + cmd_out +\
                   'Ошибки комманды: ' + cmd_err
            # send_email(mail) # подключить после настройки smtp servera'''
        else:
            cmd_time_end = datetime.datetime.now()\
                .replace(second=0, microsecond=0)
            done_task(task, cmd_time_end, cmd_out, cmd_err)
            print("Почта отправлена на e-mail")
            mail = 'Результат испонения комманды: ' + cmd_out +\
                   'Ошибки комманды: ' + cmd_err
            # send_email(mail) # подключить после настройки smtp servera'''
        print("Logger- Выполнена работа: ", task.command)
        await asyncio.sleep(1)


async def main():
    """Рефакторинг требуется, но некогда сегодня"""
    session = Session(bind=engine)
    work_queue = asyncio.Queue()
    while True:
        q = session.query(Task).\
            filter(Task.date_on == datetime.datetime.now()
                   .replace(second=0, microsecond=0))\
            .filter(Task.task_done == 'False').all()
        for work in q:
            work_queue.put_nowait(work)

        # почистим задания с неправильной датой(ошибка оператора),
        # можно обработать(выполнить, например)
        lost_tasks = session.query(Task).\
            filter(Task.date_on < datetime.datetime.now()
                   .replace(second=0, microsecond=0))\
            .filter(Task.task_done == 'False').all()

        if lost_tasks:
            for i in lost_tasks:
                session.delete(i)
                session.commit()
            print("Logger - опоздавшие задания удалены")

        await asyncio.gather(asyncio.create_task(worker("-One-", work_queue)),
                             asyncio.create_task(worker("-Two-", work_queue))
                             )


if __name__ == '__main__':
    password = parse_config().encode()
    asyncio.run(main())
