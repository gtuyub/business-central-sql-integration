from prefect.blocks.core import Block
from pydantic.v1 import SecretStr
from typing import Optional

class BCProjectConfig(Block):

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