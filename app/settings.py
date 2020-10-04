import os

# sql configuration
SQLALCHEMY_DATABASE_URI = os.environ.get('MYCLAUSE_SQL_CONNECTION_STRING', None)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# linkedin
LINKEDIN_OAUTH_CLIENT_ID = os.environ.get('MYCLAUSE_LINKEDIN_CLIENT_ID', None)
LINKEDIN_OAUTH_CLIENT_SECRET = os.environ.get('MYCLAUSE_LINKEDIN_CLIENT_SECRET', None)

# secret for login module/site
SECRET_KEY = os.environ.get('MYCLAUSE_SECRET_KEY', None)