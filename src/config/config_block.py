from prefect.blocks.core import Block
from pydantic.v1 import SecretStr
from typing import Optional

class IntegracionBusinessCentral(Block):

    tenant_id : str
    environment : str
    company_id : str
    publisher : str
    group : str
    version : str
    client_id : Optional[SecretStr]
    client_secret : Optional[SecretStr]
    username : Optional[SecretStr]
    password : Optional[SecretStr]
    server : str
    database : str