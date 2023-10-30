#!/usr/local/bin/python

from sqlalchemy import inspect
from sqlalchemy.schema import DropSchema
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import Session

from src.global_variables import ENGINE, SCHEMA
from src.models import Base

if __name__ == "__main__":
    with Session(ENGINE) as session:
        inspector = inspect(ENGINE)
        if inspector.has_schema(SCHEMA):
            session.execute(DropSchema(name=SCHEMA, cascade=True))
        session.execute(CreateSchema(name=SCHEMA))
        session.commit()

    Base.metadata.drop_all(ENGINE, checkfirst=True)
    Base.metadata.create_all(ENGINE)
