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

## Mapeo con la rúbrica

| Rúbrica | Requisito | Dónde se cumple |
|---|---|---|
| Unidad V DDL (25%) | ≥ tablas que integrantes (5) | 6 tablas (Sección 1) |
| | ≥ relaciones FK que integrantes (5) | 6 FKs (Sección 1) |
| | Completo: múltiples usuarios con permisos | 4 usuarios + GRANT (Sección 3) |
| Unidad VI DML (25%) | Base poblada antes de Python | Sección 4 (correr SQL primero) |
| | SELECT con JOIN, GROUP BY, LIKE, subconsulta | Sección 7.1–7.5 |
| | Completo: COMMIT/ROLLBACK, funciones nativas | Sección 5 (transacciones), Sección 6 (ROUND, YEAR, DATE_SUB, CURDATE) |
| Unidad VII ORM (25%) | DELETE/INSERT/SELECT/UPDATE con peewee a 2 tablas | `consultas.py` (4 funciones) |
| Documentación (25%) | Modelo lógico, físico, diccionario | Ver checklist PDF abajo |

## Checklist del PDF a armar

- [ ] Portada (integrantes, materia, docente, fecha)
- [ ] Stack tecnológico (MariaDB 12.3.3, peewee + pymysql, Python 3, GitHub)
- [ ] Modelo conceptual (notación de Chen — SIN vistas ni FKs)
- [ ] Modelo lógico (pata de gallo — SIN vistas, CON claves foráneas)
- [ ] Modelo físico (ingeniería inversa del editor, ej. HeidiSQL/DBeaver — captura PNG)
- [ ] Diccionario de datos: entidades + atributos, relaciones, vistas (las 3 de Sección 2)
- [ ] Enlace al repositorio público de GitHub
- [ ] Retrospectiva: conclusiones del parcial 1 y del parcial 2

## Pendientes del grupo

1. Crear el repo GitHub con: `gimnasio.sql`, `consultas.py`, el PDF y el PNG del DER.
2. Ajustar credenciales en `consultas.py` a su instalación local.
3. Generar el DER (PNG) con ingeniería inversa desde el editor.
4. Redactar portada, diccionario y retrospectiva.

## Notas de conversión PostgreSQL → MariaDB

- `SERIAL` → `AUTO_INCREMENT` (Int UNSIGNED).
- `JSONB` no existe en MariaDB; columnas estrictas (el parcial 2 no lo pide).
- `ENUM` es nativo en MariaDB: usado en `estado` y `metodo_pago`.
- Se mantienen el diseño, la normalización 3FN y el modelo de roles del parcial 1.
