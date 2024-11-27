from CTFd.utils.aws.constants import cognito
#this function accepts key-value dictionary of user attributes and updates the user attributes in auth provider
def update_user_attributes(access_token, attributes):
    attributes_to_update = []
    for key, value in attributes.items():
        attributes_to_update.append({
            'Name': key,
            'Value': value
        })
    payload = {
        "UserAttributes": [{'Name': 'custom:active_c', 'Value': '1'}],
        "AccessToken": access_token,
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
