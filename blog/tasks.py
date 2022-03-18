from celery import shared_task
from celery import Celery
from blogapp.celery import app

app1 = Celery()

@app1.task
def test_task():
    print(test_task.app is app1)
    print(test_task.name in app1.tasks.keys())
    print(test_task.app is app2)
    print(test_task.name in app2.tasks.keys())
    return "Done"

app2 = Celery()


@shared_task
def test_task_3():
    pass
