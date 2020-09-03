from celery import Celery

# 我们这里案例使用redis作为broker
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/8')

# 创建任务函数
@app.task
def my_task():
    print("任务函数正在执行....")