from .base import Base
from .exceptions import SQLEngineError,SQLModelsError, InsertOperationError, UpdateOperationError
import sqlalchemy
from sqlalchemy.orm import DeclarativeMeta, Session
import importlib
import inspect
import logging
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_models() -> List[DeclarativeMeta]:
    try:
        models_module = importlib.import_module('.orm_model',package='models')
        models = [cls for _,cls in inspect.getmembers(models_module,inspect.isclass) if issubclass(cls,Base) and cls is not Base]
        logger.info(f'{len(models)} SQLAlchemy base models retrieved from package.')
        models.sort(key = lambda cls: getattr(cls,'update_priority',100))
        logger.info(f'tables retrieved : {[model.__tablename__ for model in models]}')

    except Exception as e:
        raise SQLModelsError(f'Cannot retrieve the ORM models from specified module due to following error : {e}')
    return models

def create_db_engine(server,database,username,password) -> sqlalchemy.Engine:
    connection_url = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    try:
        engine = sqlalchemy.create_engine(connection_url)
        connection = engine.connect()
        connection.close()
        logger.info(f'SQLAlchemy connection with context server : "{server}" database : "{database}" tested successfully.')
        return engine
    except Exception as e:
        raise SQLEngineError(f'Cannot create database engine with context:\n server : {server} \n database : {database}\n Error : {e}')
        
def remove_duplicate_objects(model : DeclarativeMeta, main_list : List[Dict[str,str]], filter_list : List[Dict[str,str]]) -> List[Dict[str,str]]:
    if main_list and filter_list:

        p_keys = [k for k in model.__mapper__.c.keys() if getattr(model,k).primary_key]
        filter_list_index = {tuple(row[k] for k in p_keys) for row in filter_list}
        main_list = [row for row in main_list 
                if tuple(row[k] for k in p_keys) not in filter_list_index]
    
    return main_list

def insert_records(records : List[Dict[str,str]], model : DeclarativeMeta , db: Session) -> None:
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

def update_records(records : List[Dict[str,str]], model : DeclarativeMeta , db: Session) -> None:
    if records:
        #removing @odata.etag key included on every response of the API
        for item in records:
            item.pop('@odata.etag',None)
        
        try:
            logger.info('attempting bulk update operation...')
            db.bulk_update_mappings(model,records)
            logger.info(f'all records updated successfully on table {model.__tablename__}.')

        except Exception as e:
            db.rollback()
            raise UpdateOperationError(f'Could not update records from table {model.__tablename__}: {e}')
        

def get_latest_created_timestamp(model : DeclarativeMeta, db: Session) -> datetime:
    timestamp = db.query(sqlalchemy.func.max(model.systemCreatedAt)).scalar()

    return timestamp

def get_latest_modified_timestamp(model : DeclarativeMeta, db: Session) -> datetime:
    timestamp = db.query(sqlalchemy.func.max(model.systemModifiedAt)).scalar()

    return timestamp
