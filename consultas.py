"""
PARCIAL 2 — CONSULTAS DESDE PYTHON (Unidad VII: ORM)
Proyecto: Sistema de gestión de gimnasio
Integrantes: grupo de 5 (ver portada)

Las 4 consultas básicas a 2 tablas interrelacionadas (socio + inscripcion),
usando el ORM peewee con el driver pymysql (compatible con MariaDB).
Los modelos viven en models.py (compartidos con la app web Flask).

REQUISITO PREVIO: correr primero gimnasio.sql, para que la base esté
creada y POBLADA antes de ejecutar estas consultas (rúbrica Unidad VI).

Instalación de dependencias:
    pip install peewee pymysql

Antes de ejecutar, ajustar USUARIO/PASSWORD a la propia instalación
de MariaDB (los usuarios del DCL no tienen permisos de INSERT/DELETE
sobre todas las tablas; para el ORM conviene usar root o un usuario con
permisos completos).
"""

from datetime import date

from models import DB, Actividad, Inscripcion, Socio


# --- Consulta 1: SELECT con JOIN entre las 2 tablas interrelacionadas -------
def consulta_select():
    print("\n=== CONSULTA 1 — SELECT (socio JOIN inscripcion, estado activa) ===")
    query = (
        Inscripcion.select(Inscripcion, Socio, Actividad)
        .join(Socio)
        .switch(Inscripcion)
        .join(Actividad)
        .where(Inscripcion.estado == "activa")
        .order_by(Socio.apellido)
    )
    for ins in query:
        print(
            f"{ins.id_inscripcion:>3} | {ins.socio.apellido}, {ins.socio.nombre} "
            f"| {ins.actividad.nombre} | {ins.fecha_inscripcion}"
        )


# --- Consulta 2: INSERT (alta de inscripción con FK válidas) ----------------
def consulta_insert():
    print("\n=== CONSULTA 2 — INSERT (alta de inscripción) ===")
    socio = Socio.get(Socio.dni == "27890123")          # Daniela Rojas
    actividad = Actividad.get(Actividad.nombre == "Yoga-Restaurativa")

    # La FK garantiza la integridad: si el socio no existiera, el INSERT falla.
    nueva, creada = Inscripcion.get_or_create(
        socio=socio,
        actividad=actividad,
        defaults={"fecha_inscripcion": date.today(), "estado": "activa"},
    )
    if creada:
        print(
            f"INSERT OK -> id_inscripcion {nueva.id_inscripcion}: "
            f"{socio.nombre} {socio.apellido} en '{actividad.nombre}'"
        )
    else:
        print(f"Ya existía la inscripción id {nueva.id_inscripcion}, no se duplicó.")


# --- Consulta 3: UPDATE (baja lógica de la inscripción recién creada) --------
def consulta_update():
    print("\n=== CONSULTA 3 — UPDATE (baja lógica de inscripción) ===")
    socio = Socio.get(Socio.dni == "27890123")          # Daniela Rojas
    filas = (
        Inscripcion.update(estado="baja")
        .where((Inscripcion.socio == socio) & (Inscripcion.estado == "activa"))
        .execute()
    )
    print(f"UPDATE OK -> {filas} inscripción(es) pasadas a estado 'baja'.")


# --- Consulta 4: DELETE (borrado físico de la baja dada antes) --------------
def consulta_delete():
    print("\n=== CONSULTA 4 — DELETE (borrado de inscripciones en 'baja') ===")
    filas = Inscripcion.delete().where(Inscripcion.estado == "baja").execute()
    print(f"DELETE OK -> {filas} inscripción(es) eliminadas.")


def main():
    DB.connect()
    try:
        consulta_select()
        consulta_insert()
        consulta_select()
        consulta_update()
        consulta_delete()
        consulta_select()
    finally:
        DB.close()
        print("\n=== FIN — 4 consultas ejecutadas con peewee ===")


if __name__ == "__main__":
    main()
