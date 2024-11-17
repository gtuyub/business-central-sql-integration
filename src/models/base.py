from sqlalchemy.orm import DeclarativeBaseNoMeta, Session
from sqlalchemy import Column, DateTime, Integer, func, insert, update,  and_, or_,select
from datetime import datetime
from typing import List, Dict
from abc import ABC, abstractmethod
from .exceptions import InsertOperationError, UpdateOperationError

class Base(DeclarativeBaseNoMeta, ABC):
    """Base class for sqlalchemy orm models.
       Each subclass of the Base class represents a table on the sql database."""

    __abstract__ = True
    
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    systemCreatedAt = Column('created_at',DateTime)
    systemModifiedAt = Column('modified_at',DateTime)

    @classmethod
    def _get_last_created_timestamp(cls, db : Session) -> datetime:
        return db.query(func.max(cls.systemCreatedAt)).scalar()
    
    @classmethod
    def _get_last_modified_timestamp(cls, db : Session) -> datetime:
        return db.query(func.max(cls.systemModifiedAt)).scalar()
    
    @classmethod
    def get_sync_timestamps(cls, db : Session) -> dict[str,datetime]:

        return {
            'last_created' : cls._get_last_created_timestamp(db),
            'last_modified' : cls._get_last_modified_timestamp(db)
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
            
            update_keys = cls.get_update_keys()
            records_with_ids = cls._add_ids_to_update_set(update_keys, records, db)

            api_tag = '@odata.etag'
            for obj in records_with_ids:
                if api_tag in obj:
                    del obj[api_tag]
            try:

                db.execute(
                        update(cls), records_with_ids
                    )

            except Exception as e:
                raise UpdateOperationError from e

    @classmethod
    def _add_ids_to_update_set(cls, update_keys : List[str], records : List[Dict[str,str]], db : Session):

        lookup_map = {}
        for rec in records:
            lookup_map[tuple(rec[key] for key in update_keys)] = rec

        conditions = []
        for rec in records:
            record_conditions = []  
            for key in update_keys:
                record_conditions.append(getattr(cls,key) == rec[key])
            conditions.append(and_(*record_conditions))

        statement = (
            select(cls.id,*[getattr(cls,key) for key in update_keys]).where(or_(*conditions))
        )

        result = db.execute(statement).fetchall()

        records_with_ids = []

        for r in result:
            key_tuple = tuple(getattr(r,key) for key in update_keys)
            if key_tuple in lookup_map:
                original_record =   lookup_map[key_tuple].copy()
                original_record['id'] = r.id
                records_with_ids.append(original_record)

        return records_with_ids


    @classmethod
    @abstractmethod 
    def get_update_keys(cls) -> List[str]:
        """Abstract method which returns a list of attribute names representing the keys to be used on UPDATE statements."""

        return
    