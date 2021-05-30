from typing import Any

from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app.routes.api import deps
from app.core.celery_app import celery_app
from app.models import user as user_models
from app.schemas import msg as msg_schemas
from app.utils import send_test_email


router = APIRouter()


@router.post("/test-celery/", response_model=msg_schemas.Msg, status_code=201)
def test_celery(
    msg: msg_schemas.Msg,
    current_user: user_models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", response_model=msg_schemas.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: user_models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}
