#!/bin/bash
TIMECLOCK=$(cd $(dirname "${BASH_SOURCE[0]}")/../../ && pwd -P)
docker run -t -i -P \
    -v $TIMECLOCK:/home/timeclock/timeclock \
    --link timeclock_postgres:pg \
    -p 8000:8000 \
    timeclock/app \
    bash
