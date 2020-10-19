import os
import logging
from threading import Thread
from fastapi import APIRouter,BackgroundTasks
from app.worker.celery_app import celery_app
router = APIRouter()

log = logging.getLogger(__name__)

def celery_on_message(body):
    log.warn(body)

def background_on_message(task):
    log.warn(task.get(on_message=celery_on_message, propagate=False))



@router.get("/task/{word}")
async def root(word: str, background_task: BackgroundTasks):
    task_name = None

    # set correct task name based on the way you run the example
    if not bool(os.getenv('DOCKER')):
        task_name = "app.worker.celery_worker.test_celery"
    else:
        task_name = "app.app.worker.celery_worker.test_celery"

    task = celery_app.send_task(task_name, args=[word])
    print(task)
    background_task.add_task(background_on_message, task)

    return {"message": "Word received"}