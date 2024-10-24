from dataclasses import dataclass
from typing import Optional
from pathlib import Path
import os
from dotenv import load_dotenv
from prefect.blocks.core import Block
from pydantic.v1 import SecretStr

class BCIntegrationConfig(Block):

    tenant_id : str
    environment : str
    company_id : str
    publisher : str
    group : str
    version : str
    client_id : str
    client_secret : Optional[SecretStr]
    username : Optional[SecretStr]
    password : Optional[SecretStr]
    server : str
    database : str

    def get_tenant_id(self):
        return self.tenant_id
    
    def get_environment(self):
        return self.environment
    
    def get_company_id(self):
        return self.company_id
    
    def get_publisher(self):
        return self.publisher
    
    def get_group(self):
        return self.group
    
    def get_version(self):
        return self.version
    
    def get_client_id(self):
        return self.client_id
    
    def get_client_secret(self):
        return self.client_secret
    
    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password
    
    def get_server(self):
        return self.server
    
    def get_database(self):
        return self.database


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
    database : DatabaseConfig
    debug : bool = False

    @classmethod
    def from_env(cls,env_path: Optional[Path] = None) -> 'Config':

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

        return cls(api=api_config, database=db_config)
    
    @classmethod
    def from_prefect_block(cls, block_name : str, env_path: Optional[Path] = None) -> 'Config':

        try:

            block = BCIntegrationConfig.load(f'{block_name}')

        except Exception:

            cls.create_block_from_env(block_name,env_path)
            block = BCIntegrationConfig.load(f'{block_name}')

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

        return cls(api=api_config, database=db_config)
    
    @classmethod
    def create_block_from_env(cls, block_name, env_path : Optional[Path] = None):

        if env_path:
            load_dotenv(env_path)
        
        else:
            load_dotenv()

        block = BCIntegrationConfig(
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

        block.save(block_name,overwrite=True)



    

    

