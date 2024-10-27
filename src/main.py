from config.settings import Config
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional, List, Type
from models.orm_model import TablesEnum
from models.base import Base
from prefect import task, flow
from prefect.artifacts import create_table_artifact
from prefect.logging import get_run_logger
from business_central_api.client import BusinessCentralAPIClient
from business_central_api.exceptions import TokenRequestError
from models.tasks import get_all_models, create_db_engine, filter_duplicates_by_pk
from models.exceptions import SQLEngineError, ModelRetrievalError, SyncTableError


@task(task_run_name = 'sincronizar-tabla-{model.__tablename__}')
def sync_table(model : Type[Base], api_client : BusinessCentralAPIClient, db: Session):

    logger = get_run_logger()
    timestamps = model.get_sync_timestamps(db)
    model_name = model.__name__
    table_name = model.__tablename__
    fields = model.__mapper__.c.keys()

    logger.info(f'Iniciando proceso de sincronizacion.\n tabla : {table_name}')

    new_records = api_client.get_with_params(entity=model_name,last_created_at=timestamps['last_created'],select=fields)
    modified_records = api_client.get_with_params(entity=model_name,last_modified_at=timestamps['last_modified'],select=fields)
    modified_records = filter_duplicates_by_pk(model,modified_records,new_records)

    try:
        if new_records or modified_records:

            if new_records:

                logger.info(f'{len(new_records)} registros nuevos encontrados para insertar en la tabla {table_name}')
                model.insert_records(new_records, db)
                logger.info('operacion de insercion finalizada correctamente.')
                create_table_artifact(new_records, 'registros-nuevos')

            if modified_records:

                logger.info(f'{len(modified_records)} registros modificados encontrados para actualizar en la tabla {table_name}')
                model.update_records(modified_records, db)
                logger.info('operacion de actualizacion finalizada correctamente')
                create_table_artifact(modified_records,'registros-actualizados')
                
            db.commit()
        
        else:
            logger.info(f'No se encontraron registros para actualizar o modificar en la tabla {table_name}.')

    except Exception as e:
        db.rollback()
        raise SyncTableError(f'No se pudo actualizar la tabla {table_name} debido al siguiente error : {e}')
    

@flow(name='sincronizar_datos_bc_sql')
def main(config_block : Optional[str] = None, tables_filter : Optional[List[TablesEnum]] = None):

    logger = get_run_logger()
    config = Config.load_from_block(config_block) if config_block else Config.load_from_env()

    try:
        engine = create_db_engine(config.db.server,config.db.database,config.db.username,config.db.password)
        sql_session = sessionmaker(engine)
        api_client = BusinessCentralAPIClient(config.api.tenant_id,config.api.environment,config.api.publisher,
                                              config.api.group,config.api.version,config.api.company_id,
                                              config.api.client_id,config.api.client_secret)
   
        sql_tables = get_all_models(tables_filter)
        for model in sql_tables:
            with sql_session() as db:
                sync_table.submit(model,api_client,db).wait()

    except (SQLEngineError, TokenRequestError, ModelRetrievalError):
        logger.critical('No se puede ejecutar el flujo debido a un error critico.')
        raise 

    finally:
        engine.dispose()


if __name__ == '__main__':
    main()