import requests
from requests.exceptions import HTTPError
from .utils import BearerAuth, aws_auth, headers
import json
from typing import Dict, List, Union, Optional

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

        # make request
        response =  requests.get(url=url, auth=auth, verify=self.verify, headers=headers['no_body'], timeout=self.timeout)
        
        # Handle potential errors
        if response.status_code != 200:
            raise Exception(f'Failed to get references: {response.status_code} {response.text}')
        
        # return response
        return response.json()
    
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

        return response.json()
    
    ## Method for getting hash of a branch or tag
    def get_hash(self, name):
        ## use the get_all_references method to get the hash of the reference
        response = self.get_reference_details(name)
        ## loop the responses "referenes" property and return the hash property of the item with matching name and type
        return response["reference"]["hash"]
    
    ## Use this create a Brach or a Tag
    def create_reference(self, name, ref_type="BRANCH", source_reference={"name":"main", "type":"BRANCH"}):
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

        return response.json()
    
    ## Method to Create a New Commit on a Branch
    def create_commit(self, operations, branch="main", hash=None):
        hash = hash or self.get_hash(branch)
        url = self.endpoint + f'/trees/{branch}@{hash}/history/commit'
        payload = json.dumps(operations)
        auth=self.setup_auth()
        response = requests.post(url, headers=headers["has_body"], auth=auth, data=payload, verify=self.verify)

        if response.status_code != 200:
            print(response.url)
            print(response.json())
            raise Exception(f'Request failed with status {response.status_code} {response.text}')
        else:
            return response.json()
        
    ## Method to Create a Merge on a Branch
    def create_merge(self, merge, branch="main", hash=None):
        hash = hash or self.get_hash(branch)
        print(merge)
        url = self.endpoint + f'/trees/{branch}@{hash}/history/merge'
        payload = json.dumps(merge)
        auth=self.setup_auth()
        response = requests.post(url, headers=headers["has_body"], auth=auth, data=payload, verify=self.verify)

        if response.status_code != 200:
            print(response.url)
            print(response.json())
            raise Exception(f'Request failed with status {response.status_code} {response.text}')
        else:
            return response.json()
        
    ## Method to Create a Transplant on a Branch
    def create_transplant(self, transplant, branch="main", hash=None):
        hash = hash or self.get_hash(branch)
        url = self.endpoint + f'/v2/trees/{branch}@{hash}/history/transplant'
        payload = json.dumps(transplant)
        auth=self.setup_auth()
        response = requests.post(url, headers=headers["has_body"], auth=auth, data=payload, verify=self.verify)

        if response.status_code != 200:
            print(response.url)
            print(response.json())
            raise Exception(f'Request failed with status {response.status_code} {response.text}')
        else:
            return response.json()
        
    ## Method for Getting Differences Between Two References
    def get_diff(self, from_ref: str, to_ref: str, filter: Optional[str]=None, key: list=None, max_key:str=None, max_records:int=None, min_key:str=None, page_token:str=None, prefix_key:str=None):
        # Construct endpoint URL
        url = f"{self.endpoint}/trees/{from_ref}/diff/{to_ref}"

        # Construct query parameters
        params = {
            "filter": filter,
            "key": key,
            "max-key": max_key,
            "max-records": max_records,
            "min-key": min_key,
            "page-token": page_token,
            "prefix-key": prefix_key,
        }
        
        #3 Prepare Auth
        auth=self.setup_auth()

        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}

        # Make the API request
        response = requests.get(url, auth=auth, params=params)

        # If the response indicates success, return the data
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
            
    ## Method for Getting the Contents of a Reference
    def get_reference_details(self, ref: str, fetch: Optional[str] = None):
        url = f"{self.endpoint}/trees/{ref}"
        params = {}
        if fetch:
            params['fetch'] = fetch

        try:
            response = requests.get(url, params=params)
            
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            return response.json()  # Return response
        
    ## Set the hash for a reference to the hash of another reference
    def set_reference(self, ref: str, body: dict, ref_type: Optional[str] = None):
        url = f"{self.endpoint}/trees/{ref}"
        params = {}
        if ref_type:
            params['type'] = ref_type
            
        auth=self.setup_auth()

        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.put(url, json=body, params=params, headers=headers, auth=auth)

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return response.json()  # Return JSON response

    ## Method to Delete a Reference
    def delete_reference(self, ref: str, ref_type: Optional[str] = "BRANCH"):
        hash = self.get_hash(ref)
        url = f"{self.endpoint}/trees/{ref}@{hash}"
        params = {}
        auth=self.setup_auth()
        if ref_type:
            params['type'] = ref_type

        try:
            response = requests.delete(url, params=params, auth=auth)

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return response.json()  # Return JSON response

    ## Method to Get the Contents of a Reference
    def get_several_contents(self, ref: str, keys: List[str], with_doc = False):
        url = f"{self.endpoint}/trees/{ref}/contents"
        params = {
            "key": keys,
            "with-doc": with_doc
        }
        auth=self.setup_auth()
        try:
            response = requests.get(url, params=params, auth=auth)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return response.json()  # Return JSON response

    ## Method to Get the Contents of a Reference with POST
    def get_multiple_contents_post(self, ref: str, keys: List[str], with_doc: Optional[bool] = False):
        url = f"{self.endpoint}/trees/{ref}/contents"
        params = {
            "with-doc": with_doc
        }
        payload = {
            "keys": keys
        }
        auth=self.setup_auth()
        try:
            response = requests.post(url, params=params, json=payload, auth=auth)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            return response.json()  # Return JSON response

    ## Method to Get the Contents of a Reference    
    def get_content(self, ref: str, key, with_doc=False):
        # Form the URL for the endpoint
        url = f"{self.endpoint}/trees/{ref}/contents/{key}"

        # Form the query parameters
        params = {"with-doc": with_doc}
        
        auth=self.setup_auth()

        # Send the request and store the response
        response = requests.get(url, params=params, auth=auth)

        # Check the status code of the response and handle accordingly
        if response.status_code == 200:
            # If the response is successful, parse the response data
            data = response.json()
            return data

        elif response.status_code == 400:
            raise HTTPError('Invalid input, ref name not valid')

        elif response.status_code == 401:
            raise HTTPError('Invalid credentials provided')

        elif response.status_code == 403:
            raise HTTPError('Not allowed to view the given reference or read object content for a key')

        elif response.status_code == 404:
            raise HTTPError(f"Table not found on 'ref' or non-existent reference")

        else:
            response.raise_for_status()  # If the status code is anything else, raise an exception
            
    def get_entries(self, ref, content=None, filter=None, key=None, max_key=None, max_records=None, min_key=None, page_token=None, prefix_key=None):
        # Form the URL for the endpoint
        url = f"{self.endpoint}/trees/{ref}/entries"

        # Form the query parameters
        params = {
            "content": content,
            "filter": filter,
            "key": key,
            "max-key": max_key,
            "max-records": max_records,
            "min-key": min_key,
            "page-token": page_token,
            "prefix-key": prefix_key,
        }

        # Remove None values from params dictionary
        params = {k: v for k, v in params.items() if v is not None}
        auth=self.setup_auth()

        # Send the request and store the response
        response = requests.get(url, params=params, auth=auth)

        # Check the status code of the response and handle accordingly
        if response.status_code == 200:
            # If the response is successful, parse the response data
            data = response.json()
            return data

        elif response.status_code == 400:
            raise HTTPError('Invalid input, ref name not valid')

        elif response.status_code == 401:
            raise HTTPError('Invalid credentials provided')

        elif response.status_code == 403:
            raise HTTPError('Not allowed to view the given reference or fetch entries for it')

        elif response.status_code == 404:
            raise HTTPError('Ref not found')

        else:
            response.raise_for_status()  # If the status code is anything else, raise an exception
            

    ## Method to Get the Commit Log of a Reference         
    def get_commit_log(self, ref, fetch=None, filter=None, limit_hash=None, max_records=None, page_token=None):
        url = self.endpoint + f"/trees/{ref}/history"

        # construct the query parameters
        query_params = {}
        auth=self.setup_auth()
        if fetch:
            query_params['fetch'] = fetch
        if filter:
            query_params['filter'] = filter
        if limit_hash:
            query_params['limit-hash'] = limit_hash
        if max_records:
            query_params['max-records'] = max_records
        if page_token:
            query_params['page-token'] = page_token

        # send the request to the server
        response = requests.get(url, params=query_params, auth=auth)

        # check for response status
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code}, Message: {response.text}"