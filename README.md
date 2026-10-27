# Parcial 2 — Guía de entrega (gimnasio, MariaDB)

Conversión del parcial 1 (diseño en PostgreSQL) a las especificaciones del
parcial 2. Archivos de este directorio:

- `gimnasio.sql` — DDL + vistas + DCL + DML + transacciones + consultas complejas.
- `models.py` — modelos peewee compartidos (una sola definición).
- `consultas.py` — 4 consultas básicas con peewee (SELECT/INSERT/UPDATE/DELETE)
  sobre las 2 tablas interrelacionadas `socio` e `inscripcion`.
- `app.py` + `templates/` — sistema web Flask (listar, alta, inscribir, baja, eliminar).
- `iniciar_mariadb.sh` / `ejecutar.sh` / `ejecutar_web.sh` — scripts de uso.

## Cómo ejecutar

Los scripts encienden todo por sí solos: arrancan MariaDB **en modo
usuario** (sin sudo, datos en `~/.local/share/mariadb-gimnasio/`), cargan
la base si no existe y crean el entorno virtual con las dependencias
(peewee, pymysql, flask) en el primer uso.

```bash
# Sistema web (http://127.0.0.1:5000)
./ejecutar_web.sh

# Las 4 consultas de consola con peewee
./ejecutar.sh
```

### Instalación manual (alternativa)

```bash
# 1. Cargar la base (pobla y crea usuarios; reejecutable)
mariadb -u root -p < gimnasio.sql

# 2. Instalar dependencias
pip install peewee pymysql flask   # (en Arch usar un venv)

# 3. Ajustar user/password/port en models.py y ejecutar
python3 consultas.py    # consultas de consola
python3 app.py          # sistema web
```

## Restaurar la base en otra máquina

```bash
mariadb -u root -p < gimnasio_backup.sql
```

El backup incluye esquema, datos actuales, vistas y usuarios con sus
permisos. `gimnasio_backup.sql` no viaja en este repo (contraseñas en
texto plano): generarlo con

```bash
mysqldump -u root --databases gimnasio --add-drop-database > gimnasio_backup.sql
# y agregar al final la sección DCL (usuarios y GRANT)
```
