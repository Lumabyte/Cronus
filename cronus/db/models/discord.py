from sqlalchemy import Column, ForeignKey, String, BigInteger, Integer
from sqlalchemy.orm import relationship

from cronus.core.db.models import Base, AuditMixin, SoftDeleteMixin


class DiscordServer(Base, AuditMixin, SoftDeleteMixin):
    __tablename__ = "discord_servers"

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable = False)

    channels = relationship("DiscordChannel", backref="account")

    def __repr__(self):
        return f"DiscordServer(id={self.id!r}, name={self.name!r})"


class DiscordChannel(Base, AuditMixin, SoftDeleteMixin):
    __tablename__ = "discord_channels"

    id = Column(BigInteger, primary_key=True)
    server_id = Column(BigInteger, ForeignKey('DiscordServer.id'))
    type = Column(Integer, nullable=False)
    name = Column(String, nullable=False)

    server = relationship("DiscordServer", back_populates="discord_channels")

    def __repr__(self):
        return f"DiscordChannel(id={self.id!r}, server_id={self.server_id!r}, name={self.name!r})"
