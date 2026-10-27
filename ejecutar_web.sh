#!/usr/bin/env bash
# Levanta el sistema web del gimnasio (Flask) en http://127.0.0.1:5000
# Encadena: arranca MariaDB (si no corre) y luego la web.
set -e
cd "$(dirname "$0")"
./iniciar_mariadb.sh
[ -d .venv ] || { python3 -m venv .venv && .venv/bin/pip install peewee pymysql flask; }
exec .venv/bin/python3 app.py
