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
@click.option("--date", help="this help")
def insert(com, date):
    """ python client insert "ls -la" --date "2022-02-16 12:20 """
    session = Session(bind=engine)
    trans_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
    if trans_date < datetime.datetime.now().replace(second=0, microsecond=0):
        print("Задание не взято в работу - дата с опозданием")
    else:
        task = Task(
            command=com,
            date_on=date,
            task_done=False
        )
        session.add(task)
        session.commit()


@cli.command()
@click.option("--number", "-n", help="Number of upcoming tasks")
def info_next(number):
    """ python client.py info-next --number 4 """
    session = Session(bind=engine)
    try:
        q = session.query(Task)\
            .filter(Task.task_done == 'False')\
            .order_by(Task.date_on)\
            .limit(number)\
            .all()
    except Exception as e:
        print("Error: ", e)
    for task in q:
        print(task.id, task.command, task.date_on)


@cli.command()
@click.option("--number", "-n", help="Number of completed tasks")
def info_last(number):
    """ python client.py info-last --number 4 """
    session = Session(bind=engine)
    try:
        q = session.query(DoneTask)\
            .order_by(desc(DoneTask.id))\
            .limit(number)\
            .all()
    except Exception as e:
        print("Error: ", e)
    for task in q:
        print(f"Task number: {task.id}\n\tCommand: {task.command}\n\t"
              f"Start date: {task.date_on}\n\tDone: {task.date_off}\n\t"
              f"Text from the console: {task.text_out}\n\t"
              f"Error text: {task.text_err}\n")


@cli.command()
def delete_incorrect_task():
    """ delete a task with an incorrect date """
    session = Session(bind=engine)
    incorrect_tasks = session.query(Task)\
        .filter(Task.date_on < datetime.datetime.now().
                replace(second=0, microsecond=0))\
        .filter(Task.task_done == 'False')\
        .all()

    if incorrect_tasks:
        for i in incorrect_tasks:
            session.delete(i)
            session.commit()
        print("Logger - tasks with an incorrect date have been deleted")


cli.add_command(insert)

if __name__ == '__main__':
    cli()
