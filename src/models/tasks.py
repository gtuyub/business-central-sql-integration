from .base import Base
from .orm_model import Tables
from .exceptions import SQLEngineError,ModelRetrievalError
import sqlalchemy
import importlib
import inspect
import logging
from typing import List, Dict, Type, Optional, Union

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_all_models(table_filter : Optional[Union[Tables,List[Tables]]] = None) -> List[Type[Base]]:
    
    models_module = importlib.import_module('.orm_model',package='models')
    try:
        if table_filter: 
            if isinstance(table_filter,list):     
                models = [getattr(models_module,t.name) for t in table_filter]
            if isinstance(table_filter,Tables):
                models = [getattr(models_module,table_filter.name)]

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
        
def filter_duplicates_by_index(model : Type[Base], modified_records : List[Dict[str,str]], new_records : List[Dict[str,str]]) -> List[Dict[str,str]]:
    
    if modified_records and new_records:

        update_keys = model.get_update_keys()
        
        new_records_pks = {tuple(row[str(k)] for k in update_keys) for row in new_records}
        modified_records = [row for row in modified_records 
                if tuple(row[str(k)] for k in update_keys) not in new_records_pks]
    
    return modified_records
