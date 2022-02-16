import datetime

from sqlalchemy import create_engine, Integer, String, \
    Column, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@localhost:5432/lux105")
engine.connect()
Base = declarative_base()


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer(), primary_key=True)
    command = Column(String(100), nullable=False)
    date_on = Column(DateTime(), default=datetime.datetime.now()
                     .replace(second=0, microsecond=0))
    task_done = Column(Boolean(), default=False)


class DoneTask(Base):
    __tablename__ = 'donetasks'
    id = Column(Integer(), primary_key=True)
    command = Column(String(200), nullable=False)
    date_on = Column(DateTime(), default=datetime.datetime.now()
                     .replace(second=0, microsecond=0))
    date_off = Column(DateTime(), default=datetime.datetime.now()
                      .replace(second=0, microsecond=0))
    text_out = Column(Text(), default='')
    text_err = Column(Text(), default='')


if __name__ == '__main__':
    Base.metadata.create_all(engine)
