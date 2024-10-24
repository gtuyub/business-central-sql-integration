from config.settings import Config
from sqlalchemy.orm import sessionmaker, Session, DeclarativeMeta
from prefect import task, flow
from prefect.artifacts import create_table_artifact
from prefect.logging import get_run_logger
from business_central_api.client import BusinessCentralAPIClient
from business_central_api.exceptions import TokenRequestError
from models.tasks import get_models, create_db_engine, remove_duplicate_objects, insert_records, update_records, get_latest_created_timestamp, get_latest_modified_timestamp
from models.exceptions import SQLEngineError, SQLModelsError, SyncTableError


@task(task_run_name = '{model.__tablename__}')
def sync_table(model : DeclarativeMeta, api_client : BusinessCentralAPIClient, db: Session, debug : bool = False):

    logger = get_run_logger()

    last_created = get_latest_created_timestamp(model, db)
    last_modified = get_latest_modified_timestamp(model,db)
        
    model_name = model.__name__
    fields = model.__mapper__.c.keys()

    try:
        logger.info(f'Starting workflow for table : {model.__tablename__}')

        records_to_insert = api_client.get_with_params(entity = model_name,last_created_at = last_created, select = fields)   
        records_to_update = api_client.get_with_params(entity = model_name,last_modified_at = last_modified, select = fields)
        #new records appear on modified records, so this step removes the duplicates from the list to update
        records_to_update = remove_duplicate_objects(model=model,main_list=records_to_update,filter_list=records_to_insert)

        if records_to_insert: 

            logger.info(f'{len(records_to_insert)} records to insert found on entity {model_name}.')
            insert_records(records_to_insert,model,db)
            create_table_artifact(table=records_to_insert,key='inserted-records')
            logger.info(f'records inserted successfully on {model.__tablename__}')
        
        else:
            logger.info(f'There are no records to insert on table {model.__tablename__}')

        if records_to_update:

            logger.info(f'{len(records_to_update)} records to update found on entity {model_name}')
            update_records(records_to_update,model,db)
            create_table_artifact(table=records_to_update,key='updated-records')
            logger.info(f'records updated successfully on {model.__tablename__}')
        
        else:
            logger.info(f'There are no records to update on table {model.__tablename__}')

        if debug:
            db.rollback()
        else:
            db.commit()    
    except Exception as e:
        db.rollback()
        raise SyncTableError(f'Unable to sync the table {model.__tablename__}.\n Changes on the database are not applied. \n Error : {e}')

@flow(name='Database-Update')
def main():
    logger = get_run_logger() 
       
    try:
        #config = Config.from_env()
        config = Config.from_prefect_block(block_name = 'bc-integration-block')

        engine = create_db_engine(
            config.database.server,
            config.database.database,
            config.database.username,
            config.database.password
            )

        api_client = BusinessCentralAPIClient(
            config.api.tenant_id,
            config.api.environment,
            config.api.publisher,
            config.api.group,
            config.api.version,
            config.api.company_id,
            config.api.client_id,
            config.api.client_secret
            )
        
        sql_session = sessionmaker(engine)
        sql_tables = get_models()

        for model in sql_tables:
            with sql_session() as db:
                sync_table.submit(model,api_client,db).wait()

    except (SQLEngineError, TokenRequestError, SQLModelsError):
        logger.critical(f'The workflow cannot be processed due to a critical error.')
        raise 


if __name__ == '__main__':
    main()