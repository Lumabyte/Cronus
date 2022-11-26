from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from cronus.db.models import Base, AuditMixin, SoftDeleteMixin


class Account(Base, AuditMixin, SoftDeleteMixin):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    password = Column(String(100))

    attributes = relationship("AccountAttribute", backref="account")
    identities = relationship("AccountIdentity", backref="account")
    scopes = relationship("AccountScope", backref="account")

    def __repr__(self):
        return f"Account(id={self.id!r}, name={self.username!r}, password={self.password!r})"


class AccountAttribute(Base, AuditMixin, SoftDeleteMixin):
    __tablename__ = "account_attribute"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'))
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)

    def __repr__(self):
        return f"AccountAttribute(id={self.id!r}, name={self.name!r}, value={self.value!r})"


class AccountIdentity(Base, AuditMixin, SoftDeleteMixin):
    __tablename__ = "account_identity"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'))
    source = Column(String, nullable=False)
    identity = Column(String, nullable=False)
    identity_code = Column(String, nullable=True)

    def __repr__(self):
        return f"AccountIdentity(id={self.id!r}, name={self.source!r}, value={self.identity!r})"


class AccountScope(Base, AuditMixin, SoftDeleteMixin):
    __tablename__ = "account_scope"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'))
    scope = Column(String, nullable=False)

    def __repr__(self):
        return f"AccountScope(id={self.id!r}, name={self.name!r}, value={self.value!r})"
