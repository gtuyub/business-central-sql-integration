from dataclasses import dataclass
from typing import Optional
from pathlib import Path
import os
from dotenv import load_dotenv
from .config_block import IntegracionBusinessCentral

@dataclass
class APIConfig:

    tenant_id : str
    environment : str
    company_id : str
    publisher : str
    group : str
    version : str
    client_id : str
    client_secret : str


@dataclass
class DatabaseConfig:

    username : str
    password : str
    server : str
    database : str


@dataclass
class Config:
    api : APIConfig
    db : DatabaseConfig

    @classmethod
    def load_from_env(cls,env_path: Optional[Path] = None, override : bool = False) -> 'Config':

        if env_path:
            load_dotenv(env_path,override=override)
        
        else:
            load_dotenv(override=override)
        
        api_config = APIConfig(

            tenant_id = os.getenv('TENANT_ID'),
            environment = os.getenv('ENVIRONMENT'),
            company_id = os.getenv('COMPANY_ID'),
            publisher = os.getenv('API_PUBLISHER'),
            group = os.getenv('API_GROUP'),
            version = os.getenv('API_VERSION'),
            client_id = os.getenv('CLIENT_ID'),
            client_secret = os.getenv('CLIENT_SECRET')

        )

        db_config = DatabaseConfig(

            username = os.getenv('SQL_USER'),
            password = os.getenv('SQL_PASSWORD'),
            server = os.getenv('SERVER'),
            database = os.getenv('DATABASE')
        )

        return cls(api=api_config, db=db_config)
    
    @classmethod
    def load_from_block(cls, block_name : str, env_path: Optional[Path] = None) -> 'Config':

        try:
            block = IntegracionBusinessCentral.load(f'{block_name}')

        except Exception:
            cls.create_block_from_env(block_name,env_path)
            block = IntegracionBusinessCentral.load(f'{block_name}')

        api_config = APIConfig(

            tenant_id = block.tenant_id,
            environment = block.environment,
            company_id = block.company_id,
            publisher = block.publisher,
            group = block.group,
            version = block.version,
            client_id = block.client_id.get_secret_value(),
            client_secret = block.client_secret.get_secret_value()

        )

        db_config = DatabaseConfig(

            username = block.username.get_secret_value(),
            password = block.password.get_secret_value(),
            server = block.server,
            database = block.database
        )

        return cls(api=api_config, db=db_config)
    
    @classmethod
    def create_block_from_env(cls, block_name : str, env_path : Optional[Path] = None, overwrite_block : bool = False, override_env_vars : bool = False):

        if env_path:
            load_dotenv(env_path,override=override_env_vars)
        
        else:
            load_dotenv(override=override_env_vars)

        block = IntegracionBusinessCentral(
            tenant_id = os.getenv('TENANT_ID'),
            environment = os.getenv('ENVIRONMENT'),
            company_id = os.getenv('COMPANY_ID'),
            publisher = os.getenv('API_PUBLISHER'),
            group = os.getenv('API_GROUP'),
            version = os.getenv('API_VERSION'),
            client_id = os.getenv('CLIENT_ID'),
            client_secret = os.getenv('CLIENT_SECRET'),
            username = os.getenv('SQL_USER'),
            password = os.getenv('SQL_PASSWORD'),
            server = os.getenv('SERVER'),
            database = os.getenv('DATABASE')
        )
        valid_block_name = block_name.lower().replace('_','-')
        block.save(valid_block_name,overwrite=overwrite_block)



    

    

