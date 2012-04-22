from celery.task import task


@task
def find_where_to_go(planning):
    planning.find_where_to_go()
