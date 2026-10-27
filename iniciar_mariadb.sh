#!/usr/bin/env bash
# Arranca el servidor MariaDB del proyecto en modo usuario (sin sudo).
# Datos persistentes en ~/.local/share/mariadb-gimnasio
set -e
DIR="$HOME/.local/share/mariadb-gimnasio"
mkdir -p "$DIR/data"
if mariadb -S "$DIR/mariadb.sock" -u root -e "SELECT 1" >/dev/null 2>&1; then
  echo "MariaDB ya está corriendo."
else
  [ -f "$DIR/data/mysql/innodb_index_stats.ibd" ] || \
    mariadb-install-db --datadir="$DIR/data" --auth-root-authentication-method=normal > /dev/null
  nohup mariadbd --datadir="$DIR/data" --socket="$DIR/mariadb.sock" \
    --port=3306 --skip-name-resolve > "$DIR/mariadbd.log" 2>&1 &
  disown
  sleep 3
fi
[ -d "$HOME/.local/share/mariadb-gimnasio/data/gimnasio" ] || \
  mariadb -S "$DIR/mariadb.sock" -u root < "$(dirname "$0")/gimnasio.sql"
echo "Base 'gimnasio' lista en localhost:3306."
