from typing import List

import requests
from fastapi import Depends
import tables
from db import Session, get_session
from models import Topic


class Manager:
    tags: List[str] = []
    data: dict = {}
    task_tags: List[str] = []
    task_statistics: List = []

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.data = requests.get('https://codeforces.com/api/problemset.problems').json()
        self.tags = self.get_tags_from_api()
        self.tasks = self.get_tasks()
        self.task_statistics = self.get_statistics()

    def get_tags_from_api(self):
        for problem in self.data['result']['problems']:
            for tag in problem['tags']:
                if tag not in self.tags:
                    self.tags.append(tag)
        return self.tags

    def get_tasks(self):
        return self.data['result']['problems']

    def get_statistics(self):
        return self.data['result']['problemStatistics']

    def save_tags_in_db(self):
        for tag_str in self.tags:
            tag = tables.Topic(**{'name': tag_str})
            self.session.add(tag)
            self.session.commit()
        return 'Success!'

    def save_tasks_in_db(self):
        for task_data, statistics in zip(self.tasks, self.task_statistics):
            print(task_data)
            self.task_tags.append(task_data.pop('tags', []))
            task_data['solvedCount'] = statistics['solvedCount']
            task = tables.Task(**task_data)
            self.session.add(task)
            self.session.commit()
        print(self.task_tags)
        return 'Success!'

    def create_many_to_many(self):
        print(self.task_tags)
        for task, tags in zip(self.session.query(tables.Task).all(), self.task_tags):
            for tag in tags:
                tag_id = self.session.query(tables.Topic).filter_by(name=tag).first().id
                print(tag_id)
                print(task.id)
                topicInTask = {
                    'task_id': task.id,
                    'topic_id': tag_id,
                }
                tagInTask = tables.TopicInTask(**topicInTask)
                self.session.add(tagInTask)
                self.session.commit()
        return 'Success!'


class DBService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_task_by_name(self, name: str):
        task = self.session.query(tables.Task).filter_by(name=name).first()
        return task

    def get_tags_by_task(self, task_id: int) -> List[str]:
        tags_id = self.session.query(tables.TopicInTask).filter_by(task_id=task_id).all()
        print("Tags_ID:", tags_id)
        tags_name = []
        for tag_id in tags_id:
            tag = self.session.query(tables.Topic).filter_by(id=tag_id.topic_id).first()
            print(tag)
            tags_name.append(tag.name)
        return tags_name

    def get_task_by_tag(self, tag_name: str) -> List[tables.Task]:
        tag_id = self.session.query(tables.Topic).filter_by(name=tag_name).first()
        tasks_in_topic = self.session.query(tables.TopicInTask).filter_by(topic_id=tag_id.id).all()[:10]
        res_list = []
        for task in tasks_in_topic:
            task = self.session.query(tables.Task).filter_by(id=task.task_id).first()
            res_list.append(task.name)

        return res_list
