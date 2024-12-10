from CTFd.utils.aws.constants import cognito
from typing import TypedDict, Any, Optional

class Cognito_Function_Response(TypedDict, total=False):
    success: bool
    message: str
    data: Optional[Any]

class aws_user:
    def __init__(self, access_token):
        self.access_token = access_token
        pass
    #this function accepts key-value dictionary of user attributes and updates the user attributes in auth provider
    def update_user_attributes(self, attributes):
        attributes_to_update = []
        for key, value in attributes.items():
            attributes_to_update.append({
                'Name': key,
                'Value': value
            })
        payload = {
            "UserAttributes": attributes_to_update,
            "AccessToken": self.access_token,
        }
        try:
            response = cognito.update_user_attributes(**payload)
            print("User attributes updated successfully!")
            print(response)
            return {'success': True, 'message': 'User attributes updated successfully!', 'data': response}
        except cognito.exceptions.ClientError as e:
            print(e)
            print(f"Error during User attributes update process: {e.response['Error']['Message']}")
            return {'success': False, 'message': e.response['Error']['Message']}

    def send_verification_code(self, attribute_name):
        payload = {
            "AccessToken": self.access_token,
            "AttributeName":attribute_name
        }
        try:
            response = cognito.get_user_attribute_verification_code(**payload)
            return {'success': True, 'message': 'Verification code sent', 'data': response}
        except cognito.exceptions.ClientError as e:
            print(f"Error during asking for cognito attribute verification code: {e.response['Error']['Message']}")
            return {'success': False, 'message': e.response['Error']['Message']}

    def confirm_user_attribute(self, attribute_name: str, code: str) -> Cognito_Function_Response:
        payload = {
            "AccessToken": self.access_token,
            "AttributeName": attribute_name,
            "Code": code,
        }
        try:
            response = cognito.verify_user_attribute(**payload)
            return {'success': True, 'message': f'{attribute_name} confirmed successfully!', 'data': response}
        except cognito.exceptions.ClientError as e:
            print(f"Error during user attribute confirmation: {e.response['Error']['Message']}")
            return {'success': False, 'message': e.response['Error']['Message']}


    def get_user(self):
        payload = {
            "AccessToken": self.access_token,
        }
        try:
            response = cognito.get_user(**payload)
            print("User data fetched successfully!")
            user_data = self.prepare_user_data(response)
            print(response)
            return {'success': True, 'message': 'User data fetched successfully!', 'data': user_data}
        except cognito.exceptions.ClientError as e:
            print(e)
            print(f"Error during user data fetching: {e.response['Error']['Message']}")
            return {'success': False, 'message': e.response['Error']['Message']}
        
    def prepare_user_data(self, user_data):
        #loop thru user.attributes and prepare a dictionary
        user = {}
        for attribute in user_data['UserAttributes']:
            user[attribute['Name']] = attribute['Value']
        user['name'] = user_data['Username']
        return user
