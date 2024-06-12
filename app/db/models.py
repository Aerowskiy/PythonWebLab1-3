from datetime import datetime

from sqlalchemy import Column, DateTime, String, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import validates

Base: DeclarativeMeta = declarative_base()


class TimestampMixin(object):
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Users(TimestampMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)


class Orders(TimestampMixin, Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"))
    performer_id = Column(Integer, ForeignKey("users.id"))
    completed = Column(Boolean, nullable=False, default=False)


class Reviews(TimestampMixin, Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    reviewer_id = Column(Integer, ForeignKey("users.id"))

    @validates('rating')
    def validate_rating(self, key, value):
        if value not in [i for i in range(1, 6)]:
            raise ValueError('Rating must be from 1 to 5')
        return value
