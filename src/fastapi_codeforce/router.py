from typing import List

from fastapi import APIRouter, Depends
from service import Manager, DBService

router = APIRouter(
    prefix='/tasks',
    tags=['tasks']
)


@router.get('/save_all_tasks')
def save_all_tasks(service: Manager = Depends()):
    """
    Endpoint save all tasks from CODEFORCE API archive to postgresql and create intermediate table for connection
    between tags and tasks

    """
    service.save_tags_in_db()
    service.save_tasks_in_db()
    service.create_many_to_many()


@router.get('/tasks_by_tag')
def get_ten_tasks_by_tag(tag_name: str,
                         service: DBService = Depends()):
    return service.get_task_by_tag(tag_name)


@router.get('/tasks_by_name')
def get_tasks_by_name(name: str,
                      service: DBService = Depends()):
    task = service.get_task_by_name(name).__dict__
    # task.pop('_sa_instance_state', None)
    task['tags'] = service.get_tags_by_task(task_id=task['id'])
    return task
