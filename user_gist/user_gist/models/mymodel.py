from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
)

from .meta import Base


class MyModel(Base):
    __tablename__ = 'models'
    username = Column(Text, primary_key=True)
    password = Column(Text)
    email = Column(Text)
    fname = Column(Text)
    lname = Column(Text)
    fav_food = Column(Text)


Index('my_index', MyModel.username, unique=True, mysql_length=255)
