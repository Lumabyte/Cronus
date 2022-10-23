from sqlalchemy import Boolean, Column, DateTime, func


class AuditMixin():
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())


class SoftDeleteMixin():
    deleted = Column(Boolean, default=False)
