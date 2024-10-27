from .base import Base
from .orm_model import ModelsEnum
from .exceptions import SQLEngineError,ModelRetrievalError, InsertOperationError, UpdateOperationError
import sqlalchemy
import importlib
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm.exc import StaleDataError
import inspect
import logging
from typing import List, Dict, Type, Optional
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_models(models_from_enum : Optional[List[ModelsEnum]] = None) -> List[Type[DeclarativeBase]]:
    
    models_module = importlib.import_module('.orm_model',package='models')
    try:
        if models_from_enum:      
            models = [getattr(models_module,t.name) for t in models_from_enum]      
        else:
            models = [
                cls for _,cls in inspect.getmembers(models_module,inspect.isclass) 
                if issubclass(cls,Base) and cls is not Base
                ]
    except Exception as e:
        raise ModelRetrievalError(f'Cannot retrieve the SQLAlchemy models from {models_module} due to following error : {e}')   
    
    logger.info(f'Tables retrieved :\n {[model.__tablename__ for model in models]}')
    
    return models

def create_db_engine(server : str, database : str, username : str, password : str) -> sqlalchemy.Engine:

    connection_url = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    try:
        engine = sqlalchemy.create_engine(connection_url)
        connection = engine.connect()
        connection.close()
        logger.info(f'SQLAlchemy connection with context server : "{server}" database : "{database}" tested successfully.')
        return engine
    except Exception as e:
        raise SQLEngineError(f'Cannot create database engine with context:\n server : {server} \n database : {database}\n Error : {e}')
        
def remove_duplicate_objects(model : Type[DeclarativeBase], main_list : List[Dict[str,str]], filter_list : List[Dict[str,str]]) -> List[Dict[str,str]]:
    
    if main_list and filter_list:

        p_keys = [k for k in model.__mapper__.c.keys() if getattr(model,k).primary_key]
        filter_list_index = {tuple(row[k] for k in p_keys) for row in filter_list}
        main_list = [row for row in main_list 
                if tuple(row[k] for k in p_keys) not in filter_list_index]
    
    return main_list

def insert_records(records : List[Dict[str,str]], model : Type[DeclarativeBase] , db: Session) -> None:

    if records:
        #removing @odata.etag key included on every response of the API
        for item in records:
            item.pop('@odata.etag',None)
        
        try:
            logger.info('attempting bulk insert operation...')
            db.bulk_insert_mappings(model,records)
            logger.info(f'all records inserted successfully on table {model.__tablename__}.')

        except Exception as e:
            db.rollback()
            raise InsertOperationError(f'Could not insert records into table {model.__tablename__}: {e}')

def update_records(records : List[Dict[str,str]], model : Type[DeclarativeBase] , db: Session) -> None:
    
    if records:
        #removing @odata.etag key included on every response of the API
        for item in records:
            item.pop('@odata.etag',None)
        
        try:
            logger.info('attempting bulk update operation...')
            db.bulk_update_mappings(model,records)
            logger.info(f'all records updated successfully on table {model.__tablename__}.')
        
        except StaleDataError as e:
            db.rollback()
            raise StaleDataError(f'Could not update table {model.__tablename__}, this could be due to a primary key value being modified on the table : {e}')

        except Exception as e:
            db.rollback()
            raise UpdateOperationError(f'Could not update records from table {model.__tablename__}: {e}')

        
def get_latest_created_timestamp(model : Type[DeclarativeBase], db: Session) -> datetime:

    timestamp = db.query(sqlalchemy.func.max(model.systemCreatedAt)).scalar()

    return timestamp

def get_latest_modified_timestamp(model : Type[DeclarativeBase], db: Session) -> datetime:

    timestamp = db.query(sqlalchemy.func.max(model.systemModifiedAt)).scalar()

    return timestamp
