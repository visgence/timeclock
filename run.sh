#!/bin/bash

cd /home/timeclock/timeclock/time_system/time_system/clocker/static

npm install

cd /home/timeclock/timeclock/time_system/time_system

python3 manage.py makemigrations

python3 manage.py migrate

yes | python3 manage.py setup

python3 manage.py runserver 0.0.0.0:8000
