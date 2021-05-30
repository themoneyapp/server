from app.core.celery_app import celery_app


@celery_app.task(acks_late=True)  # type: ignore
def test_celery(word: str) -> str:
    return f"test task return {word}"
