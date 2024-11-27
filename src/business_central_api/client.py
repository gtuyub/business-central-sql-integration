from msal import ConfidentialClientApplication
import requests
from datetime import datetime
import urllib.parse
from typing import List
from .exceptions import BusinessCentralClientRequestError, TokenRequestError
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class BusinessCentralAPIClient(requests.Session):
    """A client for interacting with Business Central API."""
    
    def __init__(self,tenant_id,environment,api_publisher,api_group,api_version,company_id,client_id,client_secret):
        """Initializes the api client with oauth 2.0 bearer token authentication."""

        super().__init__()

        self.tenant_id = tenant_id
        self.environment = environment
        self.api_publisher = api_publisher
        self.api_group = api_group
        self.api_version = api_version
        self.company_id = company_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = ['https://api.businesscentral.dynamics.com/.default']
        self.base_url = f"https://api.businesscentral.dynamics.com/v2.0/{self.environment}/api/{self.api_publisher}/{self.api_group}/{self.api_version}/companies({self.company_id})/"
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.access_token = None
        self.token_type = None
        self.log_client_details()
        self.get_oauth_token()


        self.headers.update(
            
            {   'Authorization': f'{self.token_type} {self.access_token}',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
                }
            ) 
        
    def log_client_details(self):
        logger.info(f'Business Central Client created to interact with Web Services at: \n -API Group: {self.api_group} \n -Published By: {self.api_publisher} \n -API Version: {self.api_version}')
        logger.warning(f'Verify AL extension with this specifications is installed on the company with ID : {self.company_id}')


        
    def get_oauth_token(self):
        """Acquires bearer token by making a post request to the login endpoint for given client instance."""

        logger.info(f'Attempting to request access token at : {self.authority}')
        auth_client = ConfidentialClientApplication(client_id = self.client_id, client_credential = self.client_secret, authority = self.authority)
        response = auth_client.acquire_token_for_client(scopes = self.scopes)

        if 'access_token' in response:

            logger.info('Successfully retrieved oauth access token.')

            self.access_token = response.get('access_token')
            self.token_type = response.get('token_type')

        else:

            error = response.get('error')
            error_description = response.get('error_description')
            logger.error(f"Failed to acquire token for confidential client application. The following error was obtained in the response : \n error : {error} \n description : {error_description}")

            raise TokenRequestError(f'Unable to retrieve access token : {error_description}')
        
    def refresh_oauth_token(self):
        """Refresh the bearer token if expired"""

        self.get_oauth_token()


    def request(self, method : str, url : str, **kwargs):
        """Custom request method that handles refreshing the token if response is 401 Unauthorized."""

        endpoint = urllib.parse.urljoin(self.base_url,url)
        parameters = kwargs.get('params')
        logger.info(f'Attempting {method} request to {endpoint}. \n parameters : {parameters}')
        response = super().request(url=endpoint,method=method,**kwargs)

        logger.info(f'response obtained with status code : {response.status_code}')

        if response.status_code == 401:
            logger.warning('401 Unauthorized request, refreshing oauth token')
            self.refresh_oauth_token()
            response = super().request(url=endpoint,method=method,**kwargs)
            

        try:
            response.raise_for_status()

        except requests.HTTPError as e:
            logger.error(f'http error :\n {e}')
            raise BusinessCentralClientRequestError(f'Unable to process the request to business central API : {e}')
            

        return response
    
    
    def paginated_get_request(self, url : str, params : dict = None):
        """Paginated GET request using @odata.next link parameter, which is available on paginated responses of the API."""

        response = self.request(url=url,method='GET',headers=self.headers,params=params)
        result = response.json()

        all_values = result.get('value',[])

        next_link = result.get('@odata.nextLink')

        while next_link:

            next_response = self.request(url=next_link,method='GET',headers=self.headers)
            next_result = next_response.json()
            all_values.extend(next_result.get('value',[]))
            next_link = next_result.get('@odata.nextLink')
        
        return all_values
    
    def create_parameters(self,last_created_at : datetime = None, last_modified_at : datetime = None, order_by : str = None, select : List[str] = None, offset : int =None, limit : int = None, custom_filter : str = None):
        """Dinamically generate parameters dictionary for the request, using odata standard parameters: $filter, $orderBy, $select, $offset and $limit"""
        params = {'$schemaversion':'1.0'}

        if last_created_at:
            formatted_datetime = last_created_at.strftime('%Y-%m-%dT%H:%M:%S.%f')+'Z'
            params.update({'$filter' : f'systemCreatedAt gt {formatted_datetime}'})
        
        if last_modified_at:
            formatted_datetime = last_modified_at.strftime('%Y-%m-%dT%H:%M:%S.%f')+'Z'
            if '$filter' in params:
                params['$filter'] = params['$filter'] + f' and systemModifiedAt gt {formatted_datetime}'
            else:
                params.update({'$filter' : f'systemModifiedAt gt {formatted_datetime}'})

        if order_by:
            params.update({'$orderby' : f'{order_by}'})

        if select:
            fields = ', '.join(select)
            params.update({'$select' : f'{fields}'})

        if offset:
            params.update({ '$skip' : f'{offset}'})
        
        if limit:
            params.update({'$top' : f'{limit}'})
        
        if custom_filter:
            if '$filter' in params:
                params['$filter'] = params['$filter'] + f' and {custom_filter}'
            else:
                params.update({'$filter':f'{custom_filter}'})  
        return params

    def get_with_params(self, entity : str, last_created_at : datetime = None, last_modified_at : datetime = None, order_by : str = None, select : List[str] = None, offset : int = None, limit : int = None, custom_filter : str = None):
        """Get records from a specific API page entity, using custom odata parameters."""

        params = self.create_parameters(last_created_at,last_modified_at,order_by,select,offset,limit,custom_filter)
        result = self.paginated_get_request(url=entity,params=params)

        if result:
            logger.info(f'obtained {len(result)} items from entity {entity}.')

        else:
            logger.warning(f'No items in response for entity {entity}')

        return result
    
    def post_usd_exchange_rate(self, starting_date : str, rate_amount : float):
        """Allows to insert the exchange rate for USD currency for a specific date"""

        request_body = {
            
            'currencyCode' : 'USD',
            'relationalCurrencyCode' : '',
            'exchangeRateAmount' : rate_amount,
            'startingDate' : starting_date
        }

        response =super().request(url = urllib.parse.urljoin(self.base_url,'exchangeRates') ,method='POST', json=request_body)

        return response