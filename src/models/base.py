from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy import Column, DateTime, func, insert, update
from datetime import datetime
from typing import List, Dict
from .exceptions import InsertOperationError, UpdateOperationError


class Base(DeclarativeBase):
    """clase base de los modelos SQLAlchemy. cada una de las subclases de esta clase representa una tabla SQL en la base de datos."""

    __abstract__ = True

    systemCreatedAt = Column('created_at',DateTime)
    systemModifiedAt = Column('modified_at',DateTime)

    @classmethod
    def get_last_created_timestamp(cls, db : Session) -> datetime:
        return db.query(func.max(cls.systemCreatedAt)).scalar()
    
    @classmethod
    def get_last_modified_timestamp(cls, db : Session) -> datetime:
        return db.query(func.max(cls.systemModifiedAt)).scalar()
    
    @classmethod
    def get_sync_timestamps(cls, db : Session) -> dict[str,datetime]:

        return {
            'last_created' : cls.get_last_created_timestamp(db),
            'last_modified' : cls.get_last_modified_timestamp(db)
        }
    
    @classmethod
    def insert_records(cls, records : List[Dict[str,str]], db : Session) -> None:

        if records:

            api_tag = '@odata.etag'
            for obj in records:
                if api_tag in obj:
                    del obj[api_tag]
            try:
                db.execute(
                    insert(cls).execution_options(render_nulls=True),
                    records
                    )
            except Exception as e:
                raise InsertOperationError from e

    @classmethod
    def update_records(cls, records : List[Dict[str,str]], db : Session) -> None:

        if records:

            api_tag = '@odata.etag'
            for obj in records:
                if api_tag in obj:
                    del obj[api_tag]
            try:
                db.execute(
                    update(cls),
                    records
                )
            except Exception as e:
                raise UpdateOperationError from e