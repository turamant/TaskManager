import datetime

from sqlalchemy import desc
from sqlalchemy.orm import Session

import click

from models import Task, engine, DoneTask


@click.group()
def cli():
    pass


@cli.command()
@click.argument("com")
@click.option("--date", help="Это хелп")
def insert(com, date):
    """ python client insert "ls -la" --date "2022-02-16 12:20 """
    task = Task(
         command=com,
        date_on=date,
        task_done=False
    )
    session.add(task)
    session.commit()


@cli.command()
@click.option("--number", "-n", help="Кол-во ближайщих заданий")
def info_next(number):
    """ python client.py info-next --number 4 """
    try:
        q = session.query(Task).filter(Task.task_done == 'False')\
            .order_by(Task.date_on).limit(number).all()
    except Exception as e:
        print("Error: ", e)
    for task in q:
        print(task.id, task.command, task.date_on)


@cli.command()
@click.option("--number", "-n", help="Кол-во выполненых заданий")
def info_last(number):
    """ python client.py info-last --number 4 """
    try:
        q = session.query(DoneTask).order_by(desc(DoneTask.id))\
            .limit(number).all()
    except Exception as e:
        print("Error: ", e)
    for task in q:
        print(f"Номер задания: {task.id}\n\tКоманда: {task.command}\n\t"
              f"Дата начала: {task.date_on}\n\tВыполнено: {task.date_off}\n\t"
              f"Текст с консоли: {task.text_out}\n\t"
              f"Текст ошибок: {task.text_err}\n")


@cli.command()
def delete_incorrect_task():
    """ delete a task with an incorrect date """
    lost_tasks = session.query(Task). \
        filter(Task.date_on < datetime.datetime.now()
               .replace(second=0, microsecond=0)) \
        .filter(Task.task_done == 'False').all()

    if lost_tasks:
        for i in lost_tasks:
            session.delete(i)
            session.commit()
        print("Logger - опоздавшие задания удалены")


cli.add_command(insert)



if __name__ == '__main__':
    session = Session(bind=engine)
    cli()
