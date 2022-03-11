from celery import shared_task
from celery import Celery
from blogapp.celery import app

# app1 = Celery()

# @app1.task
# def test_task_1():
#     print(test_task_2.app is app2)
#     return "Done"

# app2 = Celery()

# @app1.task
# def test_task_2():
#     print(test_task_2.app is app2)
#     return "Done"

# @shared_task
# def test_task_3():
#     print(test_task_3.app)
#     return "Done"
