"""
PARCIAL 2 — GENERADOR DEL INFORME (DOCX)
Proyecto: Sistema de gestión de gimnasio

Genera docs/informe_parcial2.docx con:
    portada, stack tecnológico, modelo conceptual (Chen), modelo lógico
    (pata de gallo), modelo físico, diccionario de datos (entidades,
    relaciones, vistas), enlace al repositorio y retrospectiva.

Requiere haber corrido antes genera_diagramas.py.
Ejecución:
    .venv/bin/python3 generar_informe.py
"""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor

ROJO = RGBColor(0xC0, 0x39, 0x2B)
GRIS = RGBColor(0x55, 0x55, 0x55)

REPO = "https://github.com/gconcina/bd1-parcial2"
INTEGRANTES = [
    "Geronimo Concina",
    "Juan Benegas",
    "Alvaro Ñuñez",
    "Marilu Casana",
    # [COMPLETAR: 5° integrante del grupo]
]

doc = Document()
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)


def h1(texto):
    p = doc.add_heading(texto, level=1)
    for run in p.runs:
        run.font.color.rgb = ROJO
    return p


def h2(texto):
    p = doc.add_heading(texto, level=2)
    for run in p.runs:
        run.font.color.rgb = GRIS
    return p


def p(texto, negrita=False, centrado=False, cursiva=False):
    par = doc.add_paragraph()
    run = par.add_run(texto)
    run.bold = negrita
    run.italic = cursiva
    if centrado:
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return par


def tabla(filas, anchos=None):
    t = doc.add_table(rows=len(filas), cols=len(filas[0]))
    t.style = "Table Grid"
    for i, fila in enumerate(filas):
        for j, celda in enumerate(fila):
            c = t.rows[i].cells[j]
            c.text = str(celda)
            if i == 0:
                for run in c.paragraphs[0].runs:
                    run.bold = True
    return t


def imagen(ruta, ancho=6.3):
    doc.add_picture(ruta, width=Inches(ancho))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER


# ===========================================================================
# PORTADA
# ===========================================================================
for _ in range(4):
    doc.add_paragraph()
p("TRABAJO PRÁCTICO — EXAMEN PARCIAL N° 2", negrita=True, centrado=True)
t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run("Sistema de gestión de Gimnasio")
r.bold = True
r.font.size = Pt(26)
p("Base de Datos I — Tecnicatura Superior en Desarrollo de Software",
  centrado=True)
p("Instituto Superior Manuel Belgrano — Sede Godoy Cruz", centrado=True)
p("Ciclo lectivo 2026 — Presentación: 28/10/2026", centrado=True)
doc.add_paragraph()
p("Integrantes:", negrita=True, centrado=True)
for nombre in INTEGRANTES:
    p(nombre, centrado=True)
p("[COMPLETAR: 5° integrante]", centrado=True, cursiva=True)
doc.add_paragraph()
p(f"Repositorio: {REPO}", centrado=True)
doc.add_page_break()

# ===========================================================================
# I. OBJETIVO
# ===========================================================================
h1("I. Objetivo")
p(
    "El presente documento documenta y desarrolla la base de datos del "
    "sistema de gestión de un gimnasio, puliendo el diseño entregado en el "
    "primer examen parcial e implementándolo en MariaDB, con su diccionario "
    "de datos, diagramas y consultas desde Python."
)

# ===========================================================================
# II. STACK TECNOLÓGICO
# ===========================================================================
h1("II. Stack tecnológico")
tabla([
    ["Componente", "Tecnología", "Uso en el proyecto"],
    ["Motor de base de datos", "MariaDB 12.3.3", "Persistencia, DDL, DCL, DML, transacciones y vistas"],
    ["Lenguaje", "Python 3", "Consultas y sistema web"],
    ["ORM", "peewee 4.5 + pymysql", "Las 4 consultas básicas y los modelos"],
    ["Framework web", "Flask 3.1", "Sistema de gestión (alta, inscripciones, bajas)"],
    ["Control de versiones", "Git + GitHub", "Repositorio público del proyecto"],
    ["Administración", "DBeaver", "Ingeniería inversa y capturas del esquema"],
])

# ===========================================================================
# III. MODELO CONCEPTUAL
# ===========================================================================
h1("III. Modelo de datos conceptual (notación de Chen)")
p(
    "El modelo conceptual identifica 6 entidades y 5 relaciones, todas de "
    "cardinalidad 1:N. No incluye vistas ni claves foráneas: la asociación "
    "N:M entre SOCIO y ACTIVIDAD se resuelve con la entidad INSCRIPCION."
)
imagen("docs/conceptual_chen.png", 6.9)
doc.add_page_break()

# ===========================================================================
# IV. MODELO LÓGICO
# ===========================================================================
h1("IV. Modelo de datos lógico (notación pata de gallo)")
p(
    "El modelo lógico incorpora las claves foráneas que materializan las "
    "relaciones. Las vistas quedan fuera del modelo: pertenecen al nivel "
    "externo de la arquitectura ANSI-SPARC."
)
imagen("docs/logico_pata_gallo.png", 6.9)
doc.add_page_break()

# ===========================================================================
# V. MODELO FÍSICO
# ===========================================================================
h1("V. Modelo de datos físico (ingeniería inversa)")
p(
    "Diagrama generado por ingeniería inversa desde el motor, con tipos de "
    "datos de MariaDB (AUTO_INCREMENT, ENUM, DECIMAL). Puede reemplazarse "
    "por la captura del DER automático de DBeaver si se prefiere."
)
imagen("docs/fisico_der.png", 6.9)
doc.add_page_break()

# ===========================================================================
# VI. DICCIONARIO DE DATOS
# ===========================================================================
h1("VI. Diccionario de datos")

h2("6.1 Entidades con sus atributos")

entidades = {
    "SOCIO": [
        ("id_socio", "INT UNSIGNED AUTO_INCREMENT", "Clave primaria"),
        ("nombre", "VARCHAR(60)", "Nombre del socio"),
        ("apellido", "VARCHAR(60)", "Apellido del socio"),
        ("dni", "CHAR(10) UNIQUE", "Documento: identifica sin duplicados"),
        ("email", "VARCHAR(100)", "Correo de contacto"),
        ("fecha_alta", "DATE", "Fecha de ingreso al gimnasio"),
        ("activo", "TINYINT(1)", "1 = activo, 0 = inactivo (baja lógica)"),
    ],
    "PROFESOR": [
        ("id_profesor", "INT UNSIGNED AUTO_INCREMENT", "Clave primaria"),
        ("nombre", "VARCHAR(60)", "Nombre del profesor"),
        ("apellido", "VARCHAR(60)", "Apellido del profesor"),
        ("especialidad", "VARCHAR(60)", "Disciplina que enseña"),
        ("salario", "DECIMAL(10,2)", "Remuneración mensual"),
    ],
    "ACTIVIDAD": [
        ("id_actividad", "INT UNSIGNED AUTO_INCREMENT", "Clave primaria"),
        ("nombre", "VARCHAR(60)", "Nombre de la clase"),
        ("cupo_maximo", "INT UNSIGNED", "Límite de inscriptos"),
        ("monto", "DECIMAL(10,2)", "Cuota mensual de la actividad"),
        ("id_profesor", "INT UNSIGNED FK", "FK → profesor.id_profesor"),
    ],
    "INSCRIPCION": [
        ("id_inscripcion", "INT UNSIGNED AUTO_INCREMENT", "Clave primaria"),
        ("id_socio", "INT UNSIGNED FK", "FK → socio.id_socio"),
        ("id_actividad", "INT UNSIGNED FK", "FK → actividad.id_actividad"),
        ("fecha_inscripcion", "DATE", "Fecha del alta de la inscripción"),
        ("estado", "ENUM('activa','baja')", "Baja lógica: conserva el registro"),
    ],
    "PAGO": [
        ("id_pago", "INT UNSIGNED AUTO_INCREMENT", "Clave primaria"),
        ("id_socio", "INT UNSIGNED FK", "FK → socio.id_socio"),
        ("id_actividad", "INT UNSIGNED FK", "FK → actividad.id_actividad"),
        ("fecha_pago", "DATE", "Fecha en que se abonó"),
        ("monto", "DECIMAL(10,2)", "Importe abonado"),
        ("metodo_pago", "ENUM('efectivo','debito','credito')", "Medio de pago"),
    ],
    "ASISTENCIA": [
        ("id_asistencia", "INT UNSIGNED AUTO_INCREMENT", "Clave primaria"),
        ("id_inscripcion", "INT UNSIGNED FK", "FK → inscripcion.id_inscripcion"),
        ("fecha", "DATE", "Fecha del turno (única por inscripción)"),
        ("presente", "TINYINT(1)", "1 = presente, 0 = ausente"),
    ],
}
for nombre_entidad, filas in entidades.items():
    p(nombre_entidad, negrita=True)
    tabla([["Atributo", "Tipo", "Descripción"], *filas])
    doc.add_paragraph()

h2("6.2 Relaciones")
tabla([
    ["Relación", "Cardinalidad", "Implementación", "Justificación"],
    ["SOCIO — INSCRIPCION", "1:N", "FK inscripcion.id_socio",
     "Un socio se inscribe en muchas actividades"],
    ["ACTIVIDAD — INSCRIPCION", "1:N", "FK inscripcion.id_actividad",
     "Una actividad recibe muchas inscripciones (N:M resuelta por la tabla asociativa)"],
    ["PROFESOR — ACTIVIDAD", "1:N", "FK actividad.id_profesor",
     "Un profesor dicta varias actividades"],
    ["INSCRIPCION — ASISTENCIA", "1:N", "FK asistencia.id_inscripcion",
     "Una inscripción genera una asistencia por fecha"],
    ["SOCIO — PAGO", "1:N", "FK pago.id_socio",
     "Un socio acumula historial de pagos"],
])

h2("6.3 Vistas (nivel externo)")
tabla([
    ["Vista", "Rol que la consume", "Propósito"],
    ["vista_mis_datos", "Socio", "Publica solo sus inscripciones, sin datos internos"],
    ["vista_ingresos_mensuales", "Gerente", "Dashboard: pagos agrupados por año y mes"],
    ["vista_clases_disponibles", "Recepción", "Cupo ocupado y libre por actividad"],
])
p(
    "Las vistas NO figuran en los modelos conceptual ni lógico: pertenecen "
    "al nivel de vistas de la arquitectura ANSI-SPARC (tres niveles).",
    cursiva=True,
)

# ===========================================================================
# VII. REPOSITORIO
# ===========================================================================
h1("VII. Enlace al repositorio")
p("El código fuente completo está publicado en:")
p(REPO, negrita=True, centrado=True)
p(
    "Contiene: gimnasio.sql (DDL + DCL + DML + transacciones + consultas), "
    "models.py y consultas.py (ORM peewee), app.py con templates/ (sistema "
    "web Flask) y los scripts de arranque.",
)

# ===========================================================================
# VIII. RETROSPECTIVA
# ===========================================================================
h1("VIII. Retrospectiva")
h2("8.1 Conclusiones del primer examen parcial")
p(
    "[COMPLETAR: redactar las conclusiones personales del grupo sobre el "
    "avance del proyecto y el crecimiento personal al cierre del parcial 1.]",
    cursiva=True,
)
h2("8.2 Conclusiones del segundo examen parcial")
p(
    "[COMPLETAR: redactar las conclusiones personales de esta etapa: la "
    "migración del diseño a MariaDB, la implementación del ORM y la "
    "construcción del sistema web.]",
    cursiva=True,
)
p(
    "Nota para el grupo: se dejaron los espacios de las conclusiones "
    "personales sin redactar a propósito — son reflexiones individuales "
    "que cada integrante debe escribir con sus propias palabras.",
    cursiva=True,
)

doc.save("docs/informe_parcial2.docx")
print("docs/informe_parcial2.docx generado")
