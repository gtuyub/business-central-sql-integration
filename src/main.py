from business_central_api.client import BusinessCentralAPIClient
from sqlalchemy.orm import sessionmaker, Session
from models.db_model import Tables
from models.base import Base
from models.tasks import get_models_to_sync, create_db_engine, filter_duplicates_by_index
from models.exceptions import SyncTableError
from prefect import task, flow
from prefect.artifacts import create_table_artifact
from prefect.logging import get_run_logger
from config.settings import Config
from typing import Optional, List, Type


@task(task_run_name = 'sincronizar-tabla-{model.__tablename__}',log_prints=True)
def sync_table(model : Type[Base], api_client : BusinessCentralAPIClient, db: Session):
    """Syncs a specific SQL model with its API endpoint, by inserting/updating records created and modified after last sync."""
    
    logger = get_run_logger()

    table_name = model.__tablename__
    api_endpoint = model.__name__
    api_fields = model.__mapper__.c.keys()
    api_fields.remove('id')

    timestamps = model.get_sync_timestamps(db)

    logger.info(f'Iniciando proceso de sincronizacion.\n tabla : {table_name}')

    new_records = api_client.get_with_params(
        endpoint = api_endpoint,
        last_created_at = timestamps['last_created'],
        select = api_fields)

    modified_records = api_client.get_with_params(
        endpoint = api_endpoint,
        last_modified_at = timestamps['last_modified'],
        select = api_fields)

    #remove new records from list of modified records
    modified_records = filter_duplicates_by_index(model,modified_records,new_records)
    
    #if the response returns records, attempt to insert and/or update
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
    

@flow(name='sincronizar_datos_bc',log_prints=True)
def main(config_block : Optional[str] = None, table_filter : Optional[List[Tables]] = None):
    """main function, performs the sync_table function for each model."""

    logger = get_run_logger()

    try:
        #load config from prefect block on prod, from environment vars on local:
        config = Config.load_from_block(config_block) if config_block else Config.load_from_env()

        #initialize Engine, Session factory and API client:
        engine = create_db_engine(config.db.server,config.db.database,config.db.username,config.db.password)
        Session = sessionmaker(engine)
        api_client = BusinessCentralAPIClient(config.api.tenant_id,config.api.environment,config.api.publisher,
                                            config.api.group,config.api.version,config.api.company_id,
                                            config.api.client_id,config.api.client_secret)       
    except Exception as e:
        logger.critical(f'No se puede ejecutar el flujo debido a un error critico.\n {e}')
        raise 
        
    models = get_models_to_sync(table_filter)
    
    #for each model, apply sync_table function:
    for tbl in models:
        with Session() as db:
            sync_table.submit(tbl,api_client,db).wait()


if __name__ == '__main__':
    main()
    