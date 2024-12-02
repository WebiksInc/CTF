from CTFd.utils import get_app_config
import requests
from CTFd.utils.aws.auth_helpers import validate_cognito_token
def send_deployment_request(challenge_id, idToken):
    deploy_service_address = get_app_config("DEPLOY_SERVICE_ADDRESS")
    token = validate_cognito_token(idToken)
    #send deployment request to deploy_service_address
    if (token['success'] == True):
        print(token)
        payload = {
            "stage_id": "User-Agent-Bypass",
            "id_token": idToken,
        }
        url = f"{deploy_service_address}/stage/deploy-stage/"
        try:
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                raise Exception(f"Deployment request failed with status code {response.status_code}: {response.text}")
            return response.json()
        except Exception as e:
            return {'success': False, 'message': str(e)}
    else:
        raise Exception("Invalid token")

def get_external_challenges():
    deploy_service_address = get_app_config("DEPLOY_SERVICE_ADDRESS")
    url = f"{deploy_service_address}/challenges"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to get external challenges with status code {response.status_code}: {response.text}")
    return response.json()
