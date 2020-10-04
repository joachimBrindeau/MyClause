from app import sqldb

from ..models.User import User

class UserRepository:

    def get_user_id(self, user_email):
        '''
        Returns user_id of user by email, None if not found.
        '''
        user = User.query.filter_by(user_email=user_email).first()

        if user is None:
            return None

        return user.user_id

    def add_user(self, first_name, last_name, email):
        '''
        Add the user to the database with first_name, last_name and email.
        '''

        user = User(first_name, last_name, email)
        sqldb.session.add(user)
        sqldb.session.commit()

        return user