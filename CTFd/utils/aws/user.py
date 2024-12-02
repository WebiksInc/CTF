from CTFd.utils.aws.constants import cognito
#this function accepts key-value dictionary of user attributes and updates the user attributes in auth provider
class aws_user:
    def __init__(self, access_token):
        self.access_token = access_token
        pass
    
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
