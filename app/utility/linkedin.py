import logging

from functools import wraps

from flask import redirect, url_for, session
from flask_dance.contrib.linkedin import linkedin

from app import user_repository, sqldb
from app.db.models.User import User

def preferred_locale_value(multi_locale_string):
    """
    Extract the value of the preferred locale from a MultiLocaleString
    https://docs.microsoft.com/en-us/linkedin/shared/references/v2/object-types#multilocalestring
    """
    preferred = multi_locale_string["preferredLocale"]
    locale = "{language}_{country}".format(
        language=preferred["language"], country=preferred["country"]
    )
    return multi_locale_string["localized"][locale]


def protected_route(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not linkedin.authorized:
            return redirect(url_for("routes.login"))

        # ensure the user exists in the db.
        if 'user_id' not in session:
            try:
                email = linkedin.get('emailAddress?q=members&projection=(elements*(handle~))')
                email_json = email.json()
                
                user_email = None
                user_id = None

                if email_json != None:
                    user_email = email_json['elements'][0]['handle~']['emailAddress']
                    user_id = user_repository.get_user_id(user_email)
                    
                if user_id is None:
                    user = linkedin.get('me')
                    user_json = user.json()

                    if user_json != None:
                        user_firstname_localized = user_json['firstName']
                        user_lastname_localized = user_json['lastName']

                        user_firstname = preferred_locale_value(user_firstname_localized)
                        user_lastname = preferred_locale_value(user_lastname_localized)

                        # add a user to the email
                        user = user_repository.add_user(user_firstname, user_lastname, user_email)
                        user_id = user.user_id

                if user_id != None:
                    session['user_id'] = user_id
                    
            except Exception as e:
                logging.error("Couldn't parse user or email object: {}".format(e))
        
        return func(*args, **kwargs)
    return inner
