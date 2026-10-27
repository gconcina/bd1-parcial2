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

```bash
# 1. Cargar la base (pobla y crea usuarios)
mariadb < gimnasio.sql          # o: mysql -u root -p < gimnasio.sql

# 2. Instalar dependencias del ORM
pip install peewee pymysql

# 3. Ajustar user/password/port en consultas.py y ejecutar
python3 consultas.py
```
