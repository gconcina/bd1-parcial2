# Estado del proyecto — Parcial 2 (gimnasio, MariaDB)

> Archivo de seguimiento para el grupo y para retomar el trabajo en una
> sesión futura (equivale a la memoria de sesión).

## Qué está hecho

- **Base de datos** (`gimnasio.sql`): 6 tablas 3FN, 6 FKs, 4 usuarios con
  permisos (recepcionista/profesor/gerente/socio), 3 vistas, transacciones
  COMMIT/ROLLBACK, DML con funciones nativas y consultas complejas.
  Verificado ejecutándose sin errores en MariaDB 12.3.3.
- **ORM** (`models.py` + `consultas.py`): 4 consultas peewee
  (SELECT/INSERT/UPDATE/DELETE) sobre socio + inscripcion. Verificadas.
- **Web** (`app.py` + `templates/`): Flask con alta de socios, inscribir,
  baja lógica, eliminar inscripción, activar/desactivar socio y eliminar
  socio en cascada (transacción atómica). Rutas verificadas con datos reales.
- **Informe** (`docs/informe_parcial2.docx`, regenerable con
  `generar_informe.py`): portada, stack, 3 diagramas (Chen, pata de gallo,
  físico — `genera_diagramas.py`), diccionario completo, vistas, repo.
- **Repo**: https://github.com/gconcina/bd1-parcial2 (main, commits hasta
  el informe incluido).
- **Backup transportable**: `gimnasio_backup.sql` (estado actual + DCL;
  NO va al repo por contraseñas en texto plano).

## Pendientes del grupo

1. **5° integrante**: grupo de 5; se conocen Geronimo Concina, Juan
   Benegas, Alvaro Ñuñez, Marilu Casana. Falta el 5° nombre →
   regenerar portada del DOCX.
2. **Conclusiones personales** (parcial 1 y 2) en la retrospectiva del DOCX.
3. **Captura DBeaver** del DER físico (opcional: reemplaza el PNG generado;
   click derecho → Cambiar imagen en Word).
4. **Conversión a PDF** del DOCX (la hace el grupo manualmente) y entrega
   en Aula Virtual para el 28/10/2026.

## Cómo correr (una terminal, un comando)

```bash
cd ~/Descargas/gimnasio-parcial2
./ejecutar_web.sh   # MariaDB en modo usuario + web en http://127.0.0.1:5000
./ejecutar.sh       # las 4 consultas de consola
```

MariaDB corre en modo usuario (sin sudo): datos en
`~/.local/share/mariadb-gimnasio/`, puerto 3306, socket
`~/.local/share/mariadb-gimnasio/mariadb.sock`.

## Nota sobre memoria de sesión

Engram (memoria persistente) no pudo guardar en esta sesión: el workspace
de la sesión es el home (`/home/lilium`) y su escáner detecta varios repos
a la vez (powerlevel10k, remy-agenda) → ambigüedad. La próxima sesión,
abrir OpenCode desde `~/Descargas/gimnasio-parcial2` para que Engram
resuelva el proyecto `bd1-parcial2` sin ambigüedad. Este archivo cumple
el rol de memoria mientras tanto.
