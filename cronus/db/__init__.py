from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cronus.db.models import Base

# an Engine, which the Session will use for connection
# resources
engine = create_engine('sqlite:///:memory:', echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
