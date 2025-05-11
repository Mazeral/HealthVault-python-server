from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy


class Base(DeclarativeBase):
    """The base of our ORMs"""
    pass


db = SQLAlchemy(model_class=Base)
