"""
PARCIAL 2 — GENERADOR DE DIAGRAMAS (PNG)
Proyecto: Sistema de gestión de gimnasio

Genera los 3 modelos de datos que pide la documentación:
    1. conceptual_chen.png     — notación de Chen (sin vistas ni FKs)
    2. logico_pata_gallo.png   — notación pata de gallo (con FKs)
    3. fisico_der.png          — vista física tipo ingeniería inversa

Ejecución:
    .venv/bin/python3 genera_diagramas.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

ROJO = "#c0392b"
AZUL = "#2c3e50"
GRIS = "#f4f4f4"


# ---------------------------------------------------------------------------
# 1. MODELO CONCEPTUAL — NOTACIÓN DE CHEN
#    Entidades = rectángulos, atributos = elipses, relaciones = rombos.
#    No van vistas ni claves foráneas.
# ---------------------------------------------------------------------------
def chen():
    fig, ax = plt.subplots(figsize=(16, 9.5))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9.6)
    ax.axis("off")

    # entidades (x, y)
    entidades = {
        "SOCIO": (3.0, 7.6), "INSCRIPCION": (8.0, 7.6), "ACTIVIDAD": (13.0, 7.6),
        "PAGO": (3.0, 2.9), "ASISTENCIA": (8.0, 2.9), "PROFESOR": (13.0, 2.9),
    }
    # atributos: coordenadas manuales para evitar toda superposición
    atributos = {
        "SOCIO": [
            ("id_socio (PK)", (1.1, 8.9)), ("nombre", (3.0, 9.05)),
            ("apellido", (4.9, 8.9)), ("dni", (0.9, 6.35)),
            ("fecha_alta", (4.7, 6.35)), ("activo", (5.1, 5.55)),
        ],
        "INSCRIPCION": [
            ("id_inscripcion (PK)", (6.6, 8.95)),
            ("fecha_inscripcion", (8.0, 9.1)),
            ("estado", (9.4, 8.95)),
        ],
        "ACTIVIDAD": [
            ("id_actividad (PK)", (11.6, 8.9)), ("nombre", (13.0, 9.05)),
            ("cupo_maximo", (14.45, 8.85)), ("monto", (11.5, 6.35)),
        ],
        "PAGO": [
            ("id_pago (PK)", (0.75, 4.1)), ("fecha_pago", (2.25, 4.55)),
            ("monto", (3.95, 4.45)), ("metodo_pago", (5.2, 4.1)),
        ],
        "ASISTENCIA": [
            ("id_asistencia (PK)", (6.5, 4.15)), ("fecha", (8.0, 4.45)),
            ("presente", (9.45, 4.15)),
        ],
        "PROFESOR": [
            ("id_profesor (PK)", (11.25, 4.15)), ("nombre", (12.35, 4.6)),
            ("especialidad", (14.15, 4.6)), ("salario", (14.7, 3.5)),
        ],
    }
    # (rombo x,y, texto) y líneas entidad–rombo–entidad con cardinalidades
    rombos = {
        "se inscribe": (5.5, 7.6), "recibe": (10.5, 7.6),
        "realiza": (3.0, 5.25), "registra": (8.0, 5.25), "dicta": (13.0, 5.25),
    }
    conexiones = [  # (ent A, rombo, ent B, card A, card B, pos card A, pos card B)
        ("SOCIO", "se inscribe", "INSCRIPCION", "1", "N", (4.35, 7.85), (6.65, 7.85)),
        ("ACTIVIDAD", "recibe", "INSCRIPCION", "1", "N", (11.65, 7.85), (9.35, 7.85)),
        ("SOCIO", "realiza", "PAGO", "1", "N", (3.2, 6.45), (3.2, 4.05)),
        ("INSCRIPCION", "registra", "ASISTENCIA", "1", "N", (8.2, 6.45), (8.2, 4.05)),
        ("PROFESOR", "dicta", "ACTIVIDAD", "1", "N", (13.2, 4.05), (13.2, 6.45)),
    ]

    def rect(x, y, texto):
        ax.add_patch(mpatches.FancyBboxPatch(
            (x - 1.0, y - 0.45), 2.0, 0.9,
            boxstyle="round,pad=0.03", fc="white", ec=ROJO, lw=2.2, zorder=3))
        ax.text(x, y, texto, ha="center", va="center", fontsize=11,
                fontweight="bold", color=AZUL, zorder=4)

    def rombo(x, y, texto):
        ax.add_patch(mpatches.Polygon(
            [(x - 1.0, y), (x, y + 0.48), (x + 1.0, y), (x, y - 0.48)],
            closed=True, fc="#fdebd0", ec="#b9770e", lw=1.8, zorder=3))
        ax.text(x, y, texto, ha="center", va="center", fontsize=9.5,
                color="#7d5a0c", zorder=4)

    def elipse(x, y, texto):
        ax.add_patch(mpatches.Ellipse((x, y), 1.6, 0.55, fc="white",
                                      ec="#7f8c8d", lw=1.2, zorder=3))
        ax.text(x, y, texto, ha="center", va="center", fontsize=7.6,
                color=AZUL, zorder=4)

    # líneas de atributos (detrás de todo)
    for ent, lista in atributos.items():
        ex, ey = entidades[ent]
        for _, (ax_, ay_) in lista:
            ax.plot([ax_, ex], [ay_, ey], color="#bdc3c7", lw=0.9, zorder=1)

    # líneas de relaciones (detrás de rombos y entidades)
    for a, rombo_nombre, b, *_ in conexiones:
        xa, ya = entidades[a]
        xb, yb = entidades[b]
        xr, yr = rombos[rombo_nombre]
        ax.plot([xa, xr], [ya, yr], color=AZUL, lw=1.5, zorder=1)
        ax.plot([xr, xb], [yr, yb], color=AZUL, lw=1.5, zorder=1)

    for ent, (ex, ey) in entidades.items():
        rect(ex, ey, ent)
    for nombre, (xr, yr) in rombos.items():
        rombo(xr, yr, nombre)
    for ent, lista in atributos.items():
        for texto, (ax_, ay_) in lista:
            elipse(ax_, ay_, texto)

    for _, _, _, ca, cb, (px1, py1), (px2, py2) in conexiones:
        ax.text(px1, py1, ca, fontsize=11, fontweight="bold", color=ROJO, zorder=5)
        ax.text(px2, py2, cb, fontsize=11, fontweight="bold", color=ROJO, zorder=5)

    ax.set_title("Modelo conceptual — Notación de Chen (sin vistas ni FKs)",
                 fontsize=13, fontweight="bold", pad=14)
    fig.savefig("docs/conceptual_chen.png", dpi=140, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 2. MODELO LÓGICO — PATA DE GALLO (con claves foráneas, sin vistas)
# ---------------------------------------------------------------------------
def pata_gallo():
    fig, ax = plt.subplots(figsize=(15, 9))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 9)
    ax.axis("off")

    tablas = {
        "SOCIO":       (2.2, 7.0, ["PK id_socio", "nombre", "apellido", "dni", "email", "fecha_alta", "activo"]),
        "ACTIVIDAD":   (12.8, 7.0, ["PK id_actividad", "nombre", "cupo_maximo", "monto", "FK id_profesor"]),
        "INSCRIPCION": (7.5, 7.0, ["PK id_inscripcion", "FK id_socio", "FK id_actividad", "fecha_inscripcion", "estado"]),
        "PAGO":        (2.2, 2.6, ["PK id_pago", "FK id_socio", "FK id_actividad", "fecha_pago", "monto", "metodo_pago"]),
        "ASISTENCIA":  (7.5, 2.6, ["PK id_asistencia", "FK id_inscripcion", "fecha", "presente"]),
        "PROFESOR":    (12.8, 2.6, ["PK id_profesor", "nombre", "apellido", "especialidad", "salario"]),
    }
    ancho, alto_fila = 2.6, 0.30

    def caja(nombre, x, y, campos):
        h = alto_fila * (len(campos) + 1)
        ax.add_patch(mpatches.FancyBboxPatch(
            (x - ancho / 2, y - h / 2), ancho, h,
            boxstyle="round,pad=0.02", fc="white", ec=AZUL, lw=2))
        ax.add_patch(mpatches.Rectangle(
            (x - ancho / 2, y + h / 2 - alto_fila), ancho, alto_fila,
            fc=AZUL, ec=AZUL))
        ax.text(x, y + h / 2 - alto_fila / 2, nombre, ha="center", va="center",
                fontsize=10.5, fontweight="bold", color="white")
        for i, campo in enumerate(campos):
            cy = y + h / 2 - alto_fila * (i + 1.5)
            es_pk = campo.startswith("PK")
            es_fk = campo.startswith("FK")
            ax.text(x - ancho / 2 + 0.12, cy, campo, ha="left", va="center",
                    fontsize=7.8,
                    fontweight="bold" if es_pk else "normal",
                    color=ROJO if es_pk else ("#8e44ad" if es_fk else AZUL))

    for nombre, (x, y, _) in tablas.items():
        caja(nombre, x, y, _)

    def foot(E, dx, dy):
        """Pata de gallo en E (borde de la tabla 'muchos'): las 3 puntas abren
        sobre el borde de la tabla y convergen hacia la línea."""
        px, py = E[0] + 0.4 * dx, E[1] + 0.4 * dy
        ax.plot([E[0], px], [E[1] + 0.16, py], color=AZUL, lw=1.5, zorder=2)
        ax.plot([E[0], px], [E[1], py], color=AZUL, lw=1.5, zorder=2)
        ax.plot([E[0], px], [E[1] - 0.16, py], color=AZUL, lw=1.5, zorder=2)

    def one_mark(E, dx, dy):
        """Marca de 'uno' en E (borde de la tabla '1'): barra perpendicular."""
        if dx:  # línea horizontal → barra vertical
            x = E[0] + 0.18 * dx
            ax.plot([x, x], [E[1] - 0.12, E[1] + 0.12], color=AZUL, lw=1.5, zorder=2)
        else:   # línea vertical → barra horizontal
            y = E[1] + 0.18 * dy
            ax.plot([E[0] - 0.12, E[0] + 0.12], [y, y], color=AZUL, lw=1.5, zorder=2)

    # bordes reales de cada caja (ancho 2.6, filas de 0.30 + encabezado)
    # Socio(1) — Inscripcion(N): horizontal
    ax.plot([3.5, 6.2], [6.9, 6.9], color=AZUL, lw=1.6, zorder=2)
    one_mark((3.5, 6.9), 1, 0)
    foot((6.2, 6.9), -1, 0)
    # Actividad(1) — Inscripcion(N): horizontal
    ax.plot([11.5, 8.8], [6.9, 6.9], color=AZUL, lw=1.6, zorder=2)
    one_mark((11.5, 6.9), -1, 0)
    foot((8.8, 6.9), 1, 0)
    # Profesor(1) — Actividad(N): vertical (profesor top y=3.5, actividad bottom y=6.1)
    ax.plot([12.8, 12.8], [3.5, 6.1], color=AZUL, lw=1.6, zorder=2)
    one_mark((12.8, 3.5), 0, 1)
    foot((12.8, 6.1), 0, -1)
    # Inscripcion(1) — Asistencia(N): vertical (inscripcion bottom 6.1, asistencia top 3.35)
    ax.plot([7.5, 7.5], [6.1, 3.35], color=AZUL, lw=1.6, zorder=2)
    one_mark((7.5, 6.1), 0, -1)
    foot((7.5, 3.35), 0, 1)
    # Socio(1) — Pago(N): vertical (socio bottom 5.8, pago top 3.65)
    ax.plot([2.2, 2.2], [5.8, 3.65], color=AZUL, lw=1.6, zorder=2)
    one_mark((2.2, 5.8), 0, -1)
    foot((2.2, 3.65), 0, 1)

    ax.set_title("Modelo lógico — Pata de gallo (con claves foráneas, sin vistas)",
                 fontsize=13, fontweight="bold", pad=14)
    fig.savefig("docs/logico_pata_gallo.png", dpi=140, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. MODELO FÍSICO — DER automático estilo ingeniería inversa (tipos de datos)
# ---------------------------------------------------------------------------
def fisico():
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")

    tablas = {
        "socio":       (2.6, 7.1, [
            ("PK id_socio", "INT UNSIGNED AI"),
            ("nombre", "VARCHAR(60)"),
            ("apellido", "VARCHAR(60)"),
            ("dni", "CHAR(10) UQ"),
            ("email", "VARCHAR(100)"),
            ("fecha_alta", "DATE"),
            ("activo", "TINYINT(1)"),
        ]),
        "inscripcion": (7.6, 7.1, [
            ("PK id_inscripcion", "INT UNSIGNED AI"),
            ("FK id_socio", "INT UNSIGNED"),
            ("FK id_actividad", "INT UNSIGNED"),
            ("fecha_inscripcion", "DATE"),
            ("estado", "ENUM(activa,baja)"),
        ]),
        "actividad":   (13.0, 7.1, [
            ("PK id_actividad", "INT UNSIGNED AI"),
            ("nombre", "VARCHAR(60)"),
            ("cupo_maximo", "INT UNSIGNED"),
            ("monto", "DECIMAL(10,2)"),
            ("FK id_profesor", "INT UNSIGNED"),
        ]),
        "pago":        (2.6, 2.7, [
            ("PK id_pago", "INT UNSIGNED AI"),
            ("FK id_socio", "INT UNSIGNED"),
            ("FK id_actividad", "INT UNSIGNED"),
            ("fecha_pago", "DATE"),
            ("monto", "DECIMAL(10,2)"),
            ("metodo_pago", "ENUM(...)"),
        ]),
        "asistencia":  (7.6, 2.7, [
            ("PK id_asistencia", "INT UNSIGNED AI"),
            ("FK id_inscripcion", "INT UNSIGNED"),
            ("fecha", "DATE"),
            ("presente", "TINYINT(1)"),
        ]),
        "profesor":    (13.0, 2.7, [
            ("PK id_profesor", "INT UNSIGNED AI"),
            ("nombre", "VARCHAR(60)"),
            ("apellido", "VARCHAR(60)"),
            ("especialidad", "VARCHAR(60)"),
            ("salario", "DECIMAL(10,2)"),
        ]),
    }

    def caja(nombre, x, y, campos):
        alto_fila, ancho = 0.30, 3.2
        h = alto_fila * (len(campos) + 1)
        ax.add_patch(mpatches.FancyBboxPatch(
            (x - ancho / 2, y - h / 2), ancho, h,
            boxstyle="round,pad=0.02", fc="white", ec="#5d6d7e", lw=1.8))
        ax.add_patch(mpatches.Rectangle(
            (x - ancho / 2, y + h / 2 - alto_fila), ancho, alto_fila,
            fc=ROJO, ec=ROJO))
        ax.text(x, y + h / 2 - alto_fila / 2, nombre, ha="center", va="center",
                fontsize=10, fontweight="bold", color="white")
        for i, (campo, tipo) in enumerate(campos):
            cy = y + h / 2 - alto_fila * (i + 1.5)
            color = ROJO if campo.startswith("PK") else ("#8e44ad" if campo.startswith("FK") else AZUL)
            ax.text(x - ancho / 2 + 0.12, cy, campo, ha="left", va="center",
                    fontsize=7.6,
                    fontweight="bold" if color in (ROJO, "#8e44ad") else "normal",
                    color=color)
            ax.text(x + ancho / 2 - 0.12, cy, tipo, ha="right", va="center",
                    fontsize=6.8, color="#7f8c8d", style="italic")

    for nombre, (x, y, campos) in tablas.items():
        caja(nombre, x, y, campos)

    def linea(x1, y1, x2, y2, texto):
        ax.plot([x1, x2], [y1, y2], color="#5d6d7e", lw=1.5, zorder=0)
        xm, ym = (x1 + x2) / 2, (y1 + y2) / 2
        if y1 == y2:  # horizontal
            ax.text(xm, ym + 0.18, texto, ha="center", fontsize=7.5, color="#5d6d7e")
        else:         # vertical → al costado para que la línea no lo tape
            ax.text(xm + 0.28, ym, texto, ha="left", fontsize=7.5, color="#5d6d7e")

    linea(2.6 + 1.6, 6.3, 7.6 - 1.6, 6.5, "1:N")
    linea(13.0 - 1.6, 6.3, 7.6 + 1.6, 6.5, "1:N")
    linea(13.0, 4.2, 13.0, 5.4, "1:N")
    linea(7.6, 5.4, 7.6, 4.2, "1:N")
    linea(2.6, 5.4, 2.6, 4.2, "1:N")

    ax.set_title("Modelo físico — DER automático (ingeniería inversa, con tipos)",
                 fontsize=13, fontweight="bold", pad=14)
    fig.savefig("docs/fisico_der.png", dpi=140, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    import os
    os.makedirs("docs", exist_ok=True)
    chen()
    pata_gallo()
    fisico()
    print("PNGs generados en docs/: conceptual_chen.png, "
          "logico_pata_gallo.png, fisico_der.png")
