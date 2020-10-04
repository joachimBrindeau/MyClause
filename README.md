# MyClause

Project that allows for quick storing and retrieval of clauses.


## Set-up

> This project only contains the flask application.
> It does not include the devops part; setting up tls, nginx, apache, gunicorn, supervisord, ...

You'll need:
- SQL Connection String with a database for the application

### Configuration

Before starting the applications there's 2 env variables that need to be set:

```
export MYCLAUSE_SQL_CONNECTION_STRING='<insert SQL connection string>'
export MYCLAUSE_SECRET_KEY='<insert random string here>'
export MYCLAUSE_LINKEDIN_CLIENT_ID='<insert linkedin client_id>'
export MYCLAUSE_LINKEDIN_SECRET_KEY='<insert linkedin secret>'
```

in case of local development you may want to export the following environment variable to allow non-https login using linkedin:

```
export OAUTHLIB_INSECURE_TRANSPORT=1
```

Run pip3 install requirements:

```
pip3 install -r requirements.txt
```

You're ready! start the application by running

```
flask run
```