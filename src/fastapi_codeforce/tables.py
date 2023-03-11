import sqlalchemy as sa
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Task(Base):
    __tablename__ = "task"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    solvedCount = sa.Column(sa.Integer())
    name = sa.Column(sa.String(120))
    contestId = sa.Column(sa.Integer)
    index = sa.Column(sa.String(5))
    rating = sa.Column(sa.Integer())
    type = sa.Column(sa.String(50))
    points = sa.Column(sa.Float, nullable=True)


class Topic(Base):
    __tablename__ = 'topic'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(60), unique=True)


class TopicInTask(Base):
    __tablename__ = 'topicInTask'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    task_id = sa.Column(sa.ForeignKey("task.id"), primary_key=True)
    topic_id = sa.Column(sa.ForeignKey("topic.id"), primary_key=True)

    # task = relationship("Task", back_populates="topics")
    task = relationship("Task")
    # topic = relationship("Topic", back_populates="tasks")
    topic = relationship("Topic")
