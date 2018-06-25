#!/bin/bash

psql -h $PG_PORT_5432_TCP_ADDR -p $PG_PORT_5432_TCP_PORT -U timeclock -d timeclock < ~/timeclock/drop_tables.sql
echo " "
echo "==== dropped tables ====="
echo " "

psql -h $PG_PORT_5432_TCP_ADDR -p $PG_PORT_5432_TCP_PORT -U timeclock -d timeclock < $1
# NOTE: pg_restore will exit with an error on geocode_settings, which we can ignore
echo " "
echo "==== loaded test db data ===="
echo " "

