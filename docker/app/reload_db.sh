#!/bin/bash

psql -h $PG_PORT_5432_TCP_ADDR -p $PG_PORT_5432_TCP_PORT -U  timeclock -d timeclock < ~/drop_tables.sql
echo " "
echo "==== dropped tables ====="
echo " "

pg_restore -h $PG_PORT_5432_TCP_ADDR -p $PG_PORT_5432_TCP_PORT -U timeclock -d timeclock $1
echo " "
echo "==== loaded test db data ===="
echo " "