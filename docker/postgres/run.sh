#!/bin/bash
docker run -t -i -P -d \
    --name timeclock_postgres \
    -e POSTGRES_DB=timeclock \
    -e POSTGRES_USER=timeclock \
    -e POSTGRES_PASSWORD=password \
    postgres:9.2

