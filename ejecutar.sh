#!/usr/bin/env bash
# Ejecuta las 4 consultas peewee del parcial 2.
# Encadena: arranca MariaDB (si no corre) y luego corre las consultas.
set -e
cd "$(dirname "$0")"
./iniciar_mariadb.sh
[ -d .venv ] || { python3 -m venv .venv && .venv/bin/pip install peewee pymysql; }
exec .venv/bin/python3 consultas.py
