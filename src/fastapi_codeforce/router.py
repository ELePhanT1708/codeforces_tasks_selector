from typing import List
import requests_async as requests
from fastapi import APIRouter, Depends
from requests import Response

from service import Manager, DBService
from fastapi_utils.tasks import repeat_every

router = APIRouter(
    prefix='/tasks',
    tags=['tasks']
)


@router.get('/save_all_tasks_initial')
def save_all_tasks(service: Manager = Depends()):
    """
    Endpoint save all tasks from CODEFORCE API archive to postgresql and create intermediate table for connection
    between tags and tasks

    """
    service.save_tags_in_db()
    service.save_tasks_in_db()
    service.create_many_to_many()


@router.get('/update_tasks')
def update_tasks(service: Manager = Depends()):
    """

    """

    service.save_tasks_in_db()
    service.create_many_to_many()
    return 'Update success !'


######   FIX IT but I don't know how
@router.on_event('startup')
@repeat_every(seconds=60 * 60, raise_exceptions=True)
async def update_request():
    response = await requests.get('http://localhost:8000/tasks/update_tasks')
    return response


@router.get('/tasks_by_tag')
def get_ten_tasks_by_tag(tag_name: str,
                         service: DBService = Depends()):
    return service.get_tasks_by_tag(tag_name)


@router.get('/get_tags')
def get_tags(service: DBService = Depends()):
    return service.get_all_tags()


@router.get('/tasks_by_name')
def get_task_by_name(name: str,
                     service: DBService = Depends()):
    try:
        task = service.get_task_by_name(name).__dict__
        # task.pop('_sa_instance_state', None)
        task['tags'] = service.get_tags_by_task(task_id=task['id'])
        return task
    except AttributeError:
        return None


@router.get('/tasks_by_tag_and_rating')
def get_tasks_by_tag_and_rating(tag_name: str,
                                rating: int,
                                service: DBService = Depends()):
    return service.get_tasks_by_tag_and_rating(tag_name, rating)


@router.get('/get_max_contestID')
def get_tasks_by_tag_and_rating(service: DBService = Depends()):
    return service.get_max_contestID()
