"""
PARCIAL 2 — SISTEMA WEB (Flask + peewee)
Proyecto: Sistema de gestión de gimnasio
Integrantes: grupo de 5 (ver portada)

App web sobre la base 'gimnasio'. Rutas:
    GET  /                              → socios, inscripciones y actividades
    POST /socios                        → alta de socio (INSERT)
    POST /socios/<id>/inscribir         → inscripción a actividad (INSERT)
    POST /inscripciones/<id>/baja       → baja lógica (UPDATE estado='baja')
    POST /inscripciones/<id>/eliminar   → borrado físico (DELETE)

Ejecución:
    ./iniciar_mariadb.sh       # asegura el servidor y la base
    .venv/bin/python3 app.py   # http://127.0.0.1:5000
"""

from datetime import date

from flask import Flask, flash, redirect, render_template, request, url_for
from peewee import DoesNotExist

from models import Actividad, DB, Inscripcion, Pago, Socio

app = Flask(__name__)
app.secret_key = "gimnasio-parcial2-clase"


# --- Ciclo de vida de la conexión a la base (un pool por request) -----------
@app.before_request
def _db_connect():
    DB.connect(reuse_if_open=True)


@app.teardown_request
def _db_close(exc):
    if not DB.is_closed():
        DB.close()


# --- GET /: pantalla principal ----------------------------------------------
@app.route("/")
def index():
    socios = Socio.select().order_by(Socio.id_socio.asc())
    inscripciones = (
        Inscripcion.select(Inscripcion, Socio, Actividad)
        .join(Socio)
        .switch(Inscripcion)
        .join(Actividad)
        .order_by(Inscripcion.id_inscripcion.asc())
    )
    actividades = Actividad.select().order_by(Actividad.id_actividad.asc())
    return render_template(
        "index.html", socios=socios, inscripciones=inscripciones, actividades=actividades
    )


# --- POST /socios: alta de socio (INSERT) -----------------------------------
@app.route("/socios", methods=["POST"])
def alta_socio():
    nombre = request.form.get("nombre", "").strip()
    apellido = request.form.get("apellido", "").strip()
    dni = request.form.get("dni", "").strip()
    email = request.form.get("email", "").strip() or None

    if not (nombre and apellido and dni):
        flash("Nombre, apellido y DNI son obligatorios.", "error")
        return redirect(url_for("index"))

    try:
        socio = Socio.create(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            email=email,
            fecha_alta=date.today(),
        )
        flash(f"Socio {socio.nombre} {socio.apellido} dado de alta.", "ok")
    except Exception:
        # El UNIQUE(dni) de la tabla lo rechaza antes que el ORM.
        flash(f"El DNI {dni} ya está registrado.", "error")
    return redirect(url_for("index"))


# --- POST /socios/<id>/inscribir: inscripción (INSERT con FK) ----------------
@app.route("/socios/<int:id_socio>/inscribir", methods=["POST"])
def inscribir(id_socio):
    id_actividad = request.form.get("id_actividad", type=int)
    socio = Socio.get_or_none(Socio.id_socio == id_socio)
    actividad = (
        Actividad.get_or_none(Actividad.id_actividad == id_actividad)
        if id_actividad
        else None
    )
    if socio is None or actividad is None:
        flash("Socio o actividad inexistente.", "error")
        return redirect(url_for("index"))

    _, creada = Inscripcion.get_or_create(
        socio=socio,
        actividad=actividad,
        defaults={"fecha_inscripcion": date.today(), "estado": "activa"},
    )
    if creada:
        flash(f"{socio.nombre} {socio.apellido} inscripto en '{actividad.nombre}'.", "ok")
    else:
        flash(
            f"{socio.nombre} {socio.apellido} ya estaba inscripto en "
            f"'{actividad.nombre}'.",
            "error",
        )
    return redirect(url_for("index"))


# --- POST /inscripciones/<id>/baja: baja lógica (UPDATE) ---------------------
@app.route("/inscripciones/<int:id_inscripcion>/baja", methods=["POST"])
def baja_inscripcion(id_inscripcion):
    filas = (
        Inscripcion.update(estado="baja")
        .where(
            (Inscripcion.id_inscripcion == id_inscripcion)
            & (Inscripcion.estado == "activa")
        )
        .execute()
    )
    if filas:
        flash("Inscripción pasada a 'baja' (baja lógica).", "ok")
    else:
        flash("La inscripción ya estaba de baja o no existe.", "error")
    return redirect(url_for("index"))


# --- POST /inscripciones/<id>/eliminar: borrado físico (DELETE) --------------
@app.route("/inscripciones/<int:id_inscripcion>/eliminar", methods=["POST"])
def eliminar_inscripcion(id_inscripcion):
    try:
        inscripcion = Inscripcion.get(Inscripcion.id_inscripcion == id_inscripcion)
    except DoesNotExist:
        flash("La inscripción no existe.", "error")
        return redirect(url_for("index"))
    inscripcion.delete_instance()
    flash("Inscripción eliminada físicamente.", "ok")
    return redirect(url_for("index"))


# --- POST /socios/<id>/alternar: activar / desactivar socio (UPDATE) --------
@app.route("/socios/<int:id_socio>/alternar", methods=["POST"])
def alternar_socio(id_socio):
    socio = Socio.get_or_none(Socio.id_socio == id_socio)
    if socio is None:
        flash("El socio no existe.", "error")
        return redirect(url_for("index"))
    socio.activo = not socio.activo
    socio.save()
    estado = "activado" if socio.activo else "desactivado (baja lógica)"
    flash(f"Socio {socio.nombre} {socio.apellido} {estado}.", "ok")
    return redirect(url_for("index"))


# --- POST /socios/<id>/eliminar: borrado físico con dependencias (DELETE) ---
# El socio tiene FKs RESTRICT desde pago e inscripcion: se borran primero sus
# dependencias dentro de una transacción, para no dejar registros huérfanos.
@app.route("/socios/<int:id_socio>/eliminar", methods=["POST"])
def eliminar_socio(id_socio):
    socio = Socio.get_or_none(Socio.id_socio == id_socio)
    if socio is None:
        flash("El socio no existe.", "error")
        return redirect(url_for("index"))
    with DB.atomic():
        Inscripcion.delete().where(Inscripcion.socio == socio).execute()
        # sus asistencias se borran solas (FK asistencia → inscripcion CASCADE)
        Pago.delete().where(Pago.socio == socio).execute()
        socio.delete_instance()
    flash(
        f"Socio {socio.nombre} {socio.apellido} eliminado junto con sus "
        "inscripciones, pagos y asistencias.",
        "ok",
    )
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
