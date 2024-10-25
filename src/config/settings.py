from dataclasses import dataclass
from typing import Optional
from pathlib import Path
import os
from dotenv import load_dotenv
from enum import Enum
from config.settings_block import BCProjectConfig

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
    def load_from_env(cls,env_path: Optional[Path] = None) -> 'Config':

        if env_path:
            load_dotenv(env_path)
        
        else:
            load_dotenv()
        
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
            block = BCProjectConfig.load(f'{block_name}')

        except Exception:

            cls.create_block_from_env(block_name,env_path)
            block = BCProjectConfig.load(f'{block_name}')

        api_config = APIConfig(

            tenant_id = block.get_tenant_id(),
            environment = block.get_environment(),
            company_id = block.get_company_id(),
            publisher = block.get_publisher(),
            group = block.get_group(),
            version = block.get_version(),
            client_id = block.get_client_id(),
            client_secret = block.get_client_secret().get_secret_value()

        )

        db_config = DatabaseConfig(

            username = block.get_username().get_secret_value(),
            password = block.get_password().get_secret_value(),
            server = block.get_server(),
            database = block.get_database()
        )

        return cls(api=api_config, db=db_config)
    
    @classmethod
    def create_block_from_env(cls, block_name : str, env_path : Optional[Path] = None):

        if env_path:
            load_dotenv(env_path)
        
        else:
            load_dotenv()

        block = BCProjectConfig(
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
        block.save(valid_block_name,overwrite=True)



    

    

