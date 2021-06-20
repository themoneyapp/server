from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import sqltypes
from sqlalchemy.sql.schema import CheckConstraint, Column, Index, PrimaryKeyConstraint

from .utils import get_current_datetime, get_default_uuid
from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=False), default=get_default_uuid)
    created_ts = Column(sqltypes.DateTime, nullable=False, default=get_current_datetime)
    modified_ts = Column(
        sqltypes.DateTime,
        nullable=False,
        default=get_current_datetime,
        onupdate=get_current_datetime,
    )
    full_name = Column(sqltypes.String, nullable=False)
    email = Column(sqltypes.String, nullable=False)
    hashed_password = Column(sqltypes.String, nullable=False)
    is_admin = Column(sqltypes.Boolean(), default=False, nullable=False)
    is_active = Column(sqltypes.Boolean(), default=False, nullable=False)
    is_superuser = Column(sqltypes.Boolean(), default=False, nullable=False)

    __table_args__ = (
        CheckConstraint(
            (
                "(is_admin = TRUE AND is_superuser = TRUE) "
                + "OR (is_admin = TRUE AND is_superuser = FALSE) "
                + "OR (is_admin = FALSE AND is_superuser = FALSE)"
            ),
            name="check_users_is_admin_and_is_superuser",
        ),
        Index("ix_users_is_superuser", is_superuser),
        Index("ix_users_is_admin", is_admin),
        Index("ix_users_is_admin", is_admin),
        Index("uix_users_email", email, unique=True),
        PrimaryKeyConstraint("id", name="primary"),
    )
