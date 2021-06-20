from typing import Any

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app.core.celery_app import celery_app
from app.helpers.emails import send_test_email
from app.models import models_user
from app.routes.api import deps
from app.schemas import schemas_msg


router = APIRouter()


@router.post("/test-celery/", response_model=schemas_msg.Msg, status_code=201)
def test_celery(
    msg: schemas_msg.Msg,
    current_user: models_user.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", response_model=schemas_msg.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: models_user.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
