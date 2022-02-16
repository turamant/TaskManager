import asyncio
import datetime
import subprocess

from sqlalchemy.orm import Session

from models import engine, DoneTask, Task

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
        print(f"Task {name} running !!!")
        task = await work_queue.get()
        password = "a_P129bx_r"
        with subprocess.Popen(task.command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE) as cmd:
            cmd_out, cmd_err = cmd.communicate(password.encode())

        cmd_out = cmd_out.decode('utf-8')
        cmd_err = cmd_err.decode('utf-8')

        print(cmd_out, ':', cmd_err)
        print("CMD_ERR: ", cmd_err)
        print("type cmd_err: ", type(cmd_err))

        if cmd_err == b'':
            cmd_time_end = datetime.datetime.now().replace(second=0, microsecond=0)
            print("Удачно!")
            done_task(task, cmd_time_end, cmd_out, cmd_err)
        else:
            cmd_time_end = datetime.datetime.now().replace(second=0, microsecond=0)
            done_task(task, cmd_time_end, cmd_out, cmd_err)
            print("Вводи правильно комманду!!!")
            # send_email(cmd_out) # подключить после настройки smtp servera'''
        print("Выполнена работа: ", task.command)
        await asyncio.sleep(1)


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


if __name__ == '__main__':
    asyncio.run(main())