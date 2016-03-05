#!/bin/bash
TIMECLOCK=$(cd $(dirname "${BASH_SOURCE[0]}")/../../ && pwd -P)
docker run -t -i -P \
    -v $TIMECLOCK:/home/timeclock/timeclock \
    --link timeclock_postgres:pg \
    timeclock/app \
    bash
