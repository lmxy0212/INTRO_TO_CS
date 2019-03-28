#!/bin/python3
import sqlalchemy as sqa
import itertools
from db_models import Base, User, Message
connection = sqa.create_engine('sqlite+pysqlite:///p2.db')
Base.metadata.create_all(connection)





