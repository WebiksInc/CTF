import boto3
from CTFd.utils import get_app_config
cognito = boto3.client('cognito-idp', region_name='il-central-1')
def get_client_vars():
    return get_app_config("OAUTH_CLIENT_ID"), get_app_config("OAUTH_CLIENT_SECRET")

