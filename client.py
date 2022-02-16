from sqlalchemy.orm import Session

from models import Task, engine


def insert(com, date):
    """
    <   python client insert "ls -la" --date "2022-02-16 12:20"  >
    """
    task = Task(
        command=com,
        date_on=date,
        task_done=False
    )
    session.add(task)
    session.commit()

def info_next(number):
    """ <   python client.py info-next --number 4   >"""
    q = session.query(Task).filter(Task.task_done == 'False')\
        .order_by(Task.date_on).limit(number).all()
    for task in q:
        print(task.id, task.command, task.date_on)


if __name__ == '__main__':
    session = Session(bind=engine)