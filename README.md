
# Objector
Object stamina


## Documentation
https://github.com/decurgia/objector.ch/wiki


## Docker development setup
```
cd ~
git clone https://github.com/decurgia/objector.ch
docker-compose up
```

## Python Virtual Environment development setup
```
cd ~
git clone https://github.com/decurgia/objector.ch
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements-dev.txt
python3 manage.py check
```

## Configuration
Export some environment variables.

### SECRET_KEY
Set your own value, e.g. a 50 character random string.
https://docs.djangoproject.com/en/3.2/topics/signing/

```
SECRET_KEY = ''
```

### SOCIAL_AUTH_AUTH0
Setup auth0 to retrieve the below values.
https://auth0.com/docs/quickstart/webapp/django/01-login#configure-auth0

```
SOCIAL_AUTH_AUTH0_DOMAIN = '<YOUR-AUTH0-DOMAIN>'
SOCIAL_AUTH_AUTH0_KEY = '<YOUR-AUTH0-CLIENT-ID>'
SOCIAL_AUTH_AUTH0_SECRET = '<YOUR-AUTH0-CLIENT-SECRET>'
```
