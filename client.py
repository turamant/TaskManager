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


if __name__ == '__main__':
    session = Session(bind=engine)