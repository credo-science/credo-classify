#!/usr/bin/env bash

cd ..
python manage.py migrate
python manage.py initdb -u admin -p admin -t
python manage.py import -d teams -o /tmp/hh < /tmp/credo/team_mapping.json
python manage.py import -d users -o /tmp/hh < /tmp/credo/user_mapping.json
python manage.py import -d devices -o /tmp/hh < /tmp/credo/device_mapping.json
