#!/bin/bash

psql -h 127.0.0.1 -p 5432 -U  timeclock -d timeclock < ~/drop_tables.sql
echo " "
echo "==== dropped tables ====="
echo " "

pg_restore -h 127.0.0.1 -p 5432 -U timeclock -d timeclock $1
echo " "
echo "==== loaded test db data ===="
echo " "