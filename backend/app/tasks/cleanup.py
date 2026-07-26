from app.tasks.celery_app import celery_app


@celery_app.task
def cleanup_temp_files():
    # remove old temp artifacts if any
    pass