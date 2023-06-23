from botocore.credentials import get_credentials
from botocore.session import Session
from requests_aws4auth import AWS4Auth
import requests

## Custom Auth Base Class for Bearer Auth
class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
             
    def __call__(self, r):
        r.headers["Authorization"] = "bearer " + self.token
        return r
        
## Custom Function for AWS Auth
def aws_auth(region, profile):
    ## Get Credentials
    session = Session(profile=profile) # Use AWS CLI Profile
    credentials = session.get_credentials() # Get Credentials from Session
    auth = AWS4Auth(credentials.access_key, credentials.secret_key, region, "execute-api", session_token=credentials.token) # Create AWS4Auth Object
    return auth
    
## Headers for JSON
headers = {
    "has_body": {"Content-Type": "application/json"},
    "no_body": {"Accept": "application/json"}
}