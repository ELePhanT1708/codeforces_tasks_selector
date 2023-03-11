from typing import Optional

from pydantic import BaseModel


class BaseTask(BaseModel):
    name: str
    index: str
    solvedCount: int
    contestId: int
    rating: int
    type: str
    points: Optional[float]

    def __repr__(self):
        return f'< Task : {self.name} >'


class BaseTopic(BaseModel):
    name: str

    def __repr__(self):
        return f'< Topic : {self.name} >'


class BaseTopicInTask(BaseModel):
    task_id: str
    topic_id: str


class TaskCreate(BaseTask):
    pass


class TopicCreate(BaseTopic):
    pass


class TopicInTaskCreate(BaseTopicInTask):
    pass


class TaskUpdate(BaseTask):
    pass


class TopicInTaskUpdate(BaseTopicInTask):
    pass


class TopicUpdate(BaseTopic):
    pass


class Task(BaseTask):
    id: int

    class Config:
        orm_mode = True


class Topic(BaseTopic):
    id: int

    class Config:
        orm_mode = True


class TopicInTask(BaseTopicInTask):
    id: int

    class Config:
        orm_mode = True
