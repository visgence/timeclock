Timeclock
=========

A simple web application for tracking employee time.

### Dependencies
docker
All other dependencies will be handled within the docker file.

### Setup.
Clone repo
`git clone https://github.com/visgence/timeclock`
Submodule chucho
`git submodule init`
`git submodule update`

Build docker container
cd to docker/app
`./build.sh`
cd to docker/postgres
`./run.sh`
cd to root of folder
`./docker/app/run.sh`
In docker shell, setup dependencies
cd to timeclock/time_system/clocker/static
`npm install`

Setup Django
cd to timeclock/time_system
`python manage.py migrate`
`python manage.py setup`

### Running the server:
`python manage.py runserver IP:Port`

### Notes
If you decided to load fixtures in setup. You can log in with username: `admin`, password: `password`
