from sqlalchemy.orm import declarative_base
from sqlalchemy import Boolean, Column, DateTime, func


Base = declarative_base()


class AuditMixin():
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())


class SoftDeleteMixin():
    is_deleted = Column(Boolean, default=False)
