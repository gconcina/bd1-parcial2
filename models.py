"""
PARCIAL 2 — MODELOS ORM COMPARTIDOS
Proyecto: Sistema de gestión de gimnasio
Integrantes: grupo de 5 (ver portada)

Definición única de los modelos peewee que mapean las tablas creadas por
gimnasio.sql. Usado por consultas.py (consola) y app.py (web Flask).

NOTA: las contraseñas de la base van acá. Para la entrega académica es
aceptable; en un sistema real nunca van commiteadas (variables de entorno).
"""

from peewee import (
    AutoField,
    BooleanField,
    CharField,
    DateField,
    DecimalField,
    ForeignKeyField,
    IntegerField,
    Model,
    MySQLDatabase,
)

# --- Conexión a la base (ajustar credenciales a la propia instalación) ------
DB = MySQLDatabase(
    "gimnasio",
    user="root",
    password="",
    host="127.0.0.1",
    port=3306,
)


class BaseModel(Model):
    class Meta:
        database = DB


class Socio(BaseModel):
    id_socio = AutoField()
    nombre = CharField(max_length=60)
    apellido = CharField(max_length=60)
    dni = CharField(max_length=10, unique=True)
    email = CharField(max_length=100, null=True)
    fecha_alta = DateField()
    activo = BooleanField(default=True)

    class Meta:
        table_name = "socio"


class Actividad(BaseModel):
    id_actividad = AutoField()
    nombre = CharField(max_length=60)
    cupo_maximo = IntegerField()
    monto = DecimalField(max_digits=10, decimal_places=2)
    id_profesor = IntegerField()  # FK gestionada por la base, no se toca acá

    class Meta:
        table_name = "actividad"


class Inscripcion(BaseModel):
    id_inscripcion = AutoField()
    socio = ForeignKeyField(Socio, column_name="id_socio", backref="inscripciones")
    actividad = ForeignKeyField(
        Actividad, column_name="id_actividad", backref="inscripciones"
    )
    fecha_inscripcion = DateField()
    estado = CharField(max_length=10, default="activa")  # 'activa' | 'baja'

    class Meta:
        table_name = "inscripcion"


class Pago(BaseModel):
    id_pago = AutoField()
    socio = ForeignKeyField(Socio, column_name="id_socio", backref="pagos")
    actividad = ForeignKeyField(
        Actividad, column_name="id_actividad", backref="pagos"
    )
    fecha_pago = DateField()
    monto = DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = CharField(max_length=10)  # 'efectivo' | 'debito' | 'credito'

    class Meta:
        table_name = "pago"
