# CREDO-Classification

Main directory contains backend of app. Is written in Python with Django framework.

Frontend is stored in `./frontend` directory. Please read [here](frontend/README.md).

## Getting started

How to install dependency libraries and run project.

### Requirements

1. Python (tested on v3.6 and v3.7)
2. Database compatible with Django ORM, tested on PostgreSQL v10 and v11

### Configuration

No should not be necessary to modification `credo_classification/settings.py`.
All local settings should be set by environment variables:
* `CREDO_SECRET` - unique secret, default: `xxx`
* `CREDO_DEBUG` - set `1` to run in debug mode, when it will not be redirect to HTTPS, default: `0`
* `CREDO_ENDPOINT` - base URL over root of domain, without slash on start, default: `user-interface/classification/`
* `CREDO_SERVER` - endpoint to [CREDO storage API](https://github.com/credo-science/credo-webapp) instance, default: `https://api.credo.science/`
* `CREDO_DEPLOY_SITE` - used for introduce during communication with [CREDO storage API](https://github.com/credo-science/credo-webapp), **please set** to your name when you connect with `https://api.credo.science/` instead local instance.
* `CREDO_DB_*` - database settings redirected to Django ORM settings, support and default values:
  * `CREDO_DB_ENGINE` - `django.db.backends.postgresql`
  * `CREDO_DB_NAME` - `credo`
  * `CREDO_DB_PASSWORD` - `credo`
  * `CREDO_DB_HOST` - `127.0.0.1`
  * `CREDO_DB_PORT` - `5432`

All settings is optional.


### Install dependency

```shell script
$ python -m venv venv
$ source venv/bin/activate
$ pip install pip --upgrade
$ pip install -r requirements.txt
```

### Prepare to run

Please go to `./frontend` directory and build production version of frontend. Then:

```shell script
$ python manage.py migrate
$ python manage.py initdb -u {admin_user} -p {admin_password} -t
$ python manage.py collectstatic
```

**Warning** Please not use the `-t` parameter for `initdb` in production. It cause create authorization token filled by zeros for admin user. It is very dangerous security backdoor. 
 
### Run

```shell script
$ python manage.py runserver
```

or via Daphne server:

```shell script
$ daphne -b 0.0.0.0 -p 80 credo_classification.asgi:application
```
