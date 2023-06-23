import requests
from utils import BearerAuth, aws_auth, headers
import json

class NessieV2Client:
    def __init__ (self, config):
        ## Add config properties to instance
        self.endpoint = config.get('endpoint', '')
        self.auth = config.get('auth', '')
        self.verify = config.get('verify', '')
        self.default_branch = config.get('default_branch', 'main')
        self.timeout = config["auth"].get("timeout", 10) 
        
    ## Method to return proper auth headers    
    def setup_auth(self):
        ## Get Auth Type
        type = self.auth.get('type', 'none').lower()
        
        ## If Auth is Set to None
        if(type == 'none'):
            return None
        ## If Auth is Set to Bearer
        if(type == 'bearer'):
            token = self.auth.get('token', '')
            return BearerAuth(token)
        ## If Auth is Set to AWS
        if(type == 'aws'):
            region = self.auth.get('region', '')
            profile = self.auth.get('profile', '')
            return aws_auth(region, profile)
        ## If Auth is Set to Basic
        if(type == 'basic'):
            username = self.auth.get('username', '')
            password = self.auth.get('password', '')
            return requests.auth.HTTPBasicAuth(username, password)
        
        ## If Unsupported Auth Type
        raise NotImplementedError("Unsupported authentication type: " + type)
    
    ## Used to configuration details
    def get_config(self):
        url = self.endpoint + '/config'
        auth = self.setup_auth()
        return requests.get(url=url, auth=auth, verify=self.verify, headers=headers['no_body'], timeout=self.timeout)
    
    ## Use this to get a list of branches and tags
    def get_all_references(self, fetch=None, filter=None, max_records=None, page_token=None):
        """
        Get information about all branches and tags in the Nessie repository.

        Parameters:
        fetch: Specifies how much extra information is to be retrieved from the server.
        filter: A Common Expression Language (CEL) expression to filter the results.
        max_records: Maximum number of entries to return.
        page_token: Paging continuation token.

        Returns:
        The server's response as a JSON object.
        """
        url = f"{self.endpoint}/trees"
        params = {
            "fetch": fetch,
            "filter": filter,
            "max-records": max_records,
            "page-token": page_token
        }

        # Remove any parameters that weren't provided
        params = {k: v for k, v in params.items() if v is not None}
        
        auth=self.setup_auth()

        response = requests.get(url, params=params, auth=auth, headers=headers["no_body"], verify=self.verify)

        # Handle potential errors
        if response.status_code != 200:
            raise Exception(f'Failed to get references: {response.status_code} {response.text}')

        return response
    
    
    ## Use this create a Brach or a Tag
    def create_reference(self, name, ref_type="BRANCH", source_reference={"name":"main"}):
        """
        Create a new branch or tag in the Nessie repository.

        Parameters:
        name: Name of the new branch or tag
        ref_type: Type of the new reference ('BRANCH' or 'TAG')
        source_reference: Source reference data (should be a dictionary representing the reference object)

        Returns:
        The server's response as a JSON object.
        """
        url = f"{self.endpoint}/trees"
        params = {
            "name": name,
            "type": ref_type.upper()
        }
        auth = self.setup_auth()

        response = requests.post(url, params=params, auth=auth, headers=headers["has_body"], data=json.dumps(source_reference), verify=self.verify)

        # Handle potential errors
        if response.status_code != 200:
            raise Exception(f'Failed to create reference: {response.status_code} {response.text}')

        return response
    
    ## Method to Create a New Commit on a Branch
    def create_commit(self, branch, operations, expected_hash=None):
        url = self.endpoint + f'/trees/{branch}/history/commit'
        payload = json.dumps(operations)
        params = {"expected_hash": expected_hash}
        auth=self.setup_auth()
        response = requests.post(url, headers=headers["has_body"], params=params, auth=auth, data=payload, verify=self.verify)

        if response.status_code != 200:
            print(response.json())
            raise Exception(f'Request failed with status {response.status_code}')
        else:
            return response