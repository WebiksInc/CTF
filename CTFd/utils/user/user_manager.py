from CTFd.models import Users
from CTFd.utils.aws.user import aws_user


class UserManager(Users):
    def __init__(self, user_id, access_token):
        # Initialize the parent class (Users)
        super().__init__()

        # Collect user data from Cognito and DB
        db_user = Users.query.filter_by(id=user_id).first()
        self.idp_user_instance = aws_user(access_token)
        idp_user = self.idp_user_instance.get_user()['data']

        # Assign attributes from idp_user
        idp_fields = ['name', 'email','custom:current_challenge' 'type', 'secret', 'website', 'affiliation', 'country', 'hidden', 'banned', 'verified', 'language']
        for field in idp_fields:
            if field.startswith('custom:'):
                 # Strip the 'custom:' prefix
                setattr(self, field[7:], idp_user.get(field, ''))
            else:
                setattr(self, field, idp_user.get(field, ''))

        # Assign attributes from db_user
        db_fields = ['id', 'bracket_id', 'team_id', 'created']
        for field in db_fields:
            setattr(self, field, getattr(db_user, field))

    # Additional methods specific to UserManager
    def update_user_attributes(self, attributes):
        return self.idp_user_instance.update_user_attributes(attributes)


def getUserIdFromCognitoSub(userSub):
    user = Users.query.filter_by(cognito_id=userSub).first()
    if user:
        return user.id
    return None
