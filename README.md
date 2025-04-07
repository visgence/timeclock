# Timeclock

A simple web application for tracking employee time.

### Dependencies

docker, nodejs
OPTIONAL - podman and podman-compose
All other dependencies will be handled within the docker file.

### Setup (docker compose OR podman-compose)

Clone repo  
`git clone https://github.com/visgence/timeclock`
Submodule chucho  
`git submodule init`  
`git submodule update`

copy `.env-template` to `.env` and edit with passwords

run `docker compose build` and `docker compose up` from base directory
OR
run `podman-compose build` and `podman-compose up` from base directory

go to `localhost:8000` in browser

You can log in with username: `admin`, password: `password`

### Reset database

run `docker compose down`
run `docker volume rm timeclock_pgdata`

### Disable Jobs

In `settings.py` set `ENABLE_JOBS` to `False`  
Running `python manage.py setup` will set up the required default job

### Custom Branding

Replace `time_system/clocker/static/images/logo.png` with your png logo file
