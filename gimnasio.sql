-- ============================================================================
--  PARCIAL 2 — BASE DE DATOS INTEGRADOR
--  Proyecto: Sistema de gestión de gimnasio
--  Motor: MariaDB 12.3.3
--  Integrantes: grupo de 5 (ver portada)
-- ============================================================================
--  Este archivo contiene, en orden:
--    SECCIÓN 0: Preparación (reejecutable)
--    SECCIÓN 1: DDL — creación de base y tablas con claves foráneas
--    SECCIÓN 2: Vistas por rol (nivel de vistas ANSI-SPARC)
--    SECCIÓN 3: DCL — creación de usuarios y permisos
--    SECCIÓN 4: DML — carga de datos (ANTES de las consultas Python)
--    SECCIÓN 5: Transacciones (COMMIT y ROLLBACK)
--    SECCIÓN 6: DML avanzado (funciones nativas en UPDATE/DELETE/INSERT)
--    SECCIÓN 7: Consultas complejas (JOIN, GROUP BY, LIKE, subconsulta)
-- ============================================================================
--  Notas de la conversión desde el parcial 1 (PostgreSQL → MariaDB):
--    * SERIAL de PostgreSQL se reemplaza por AUTO_INCREMENT (idiomático).
--    * JSONB no existe en MariaDB; se omitió a favor de columnas estrictas.
--    * ENUM es nativo aquí, se usa para estado/metodo_pago.
--    * El diseño, las relaciones y la normalización 3FN se mantienen.
-- ============================================================================

-- ============================================================================
--  SECCIÓN 0 — PREPARACIÓN
--  Deja la base en estado limpio para reejecutar el script completo.
-- ============================================================================

SET FOREIGN_KEY_CHECKS = 0;
DROP DATABASE IF EXISTS gimnasio;
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================================
--  SECCIÓN 1 — DDL: CREACIÓN DE TABLAS
--  6 tablas (>= integrantes del grupo) y 5 relaciones por clave foránea.
-- ============================================================================

CREATE DATABASE gimnasio
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE gimnasio;

-- ---- PROFESOR --------------------------------------------------------------
CREATE TABLE profesor (
  id_profesor   INT UNSIGNED NOT NULL AUTO_INCREMENT,
  nombre        VARCHAR(60)  NOT NULL,
  apellido      VARCHAR(60)  NOT NULL,
  especialidad  VARCHAR(60)  NOT NULL,
  salario       DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (id_profesor)
) ENGINE=InnoDB;

-- ---- SOCIO -----------------------------------------------------------------
CREATE TABLE socio (
  id_socio    INT UNSIGNED NOT NULL AUTO_INCREMENT,
  nombre      VARCHAR(60)  NOT NULL,
  apellido    VARCHAR(60)  NOT NULL,
  dni         CHAR(10)     NOT NULL UNIQUE,
  email       VARCHAR(100),
  fecha_alta  DATE         NOT NULL,
  activo      TINYINT(1)   NOT NULL DEFAULT 1,
  PRIMARY KEY (id_socio)
) ENGINE=InnoDB;

-- ---- ACTIVIDAD (FK → profesor) --------------------------------------------
CREATE TABLE actividad (
  id_actividad INT UNSIGNED NOT NULL AUTO_INCREMENT,
  nombre       VARCHAR(60)  NOT NULL,
  cupo_maximo  INT UNSIGNED NOT NULL,
  monto        DECIMAL(10,2) NOT NULL,
  id_profesor  INT UNSIGNED NOT NULL,
  PRIMARY KEY (id_actividad),
  CONSTRAINT fk_actividad_profesor
    FOREIGN KEY (id_profesor) REFERENCES profesor (id_profesor)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ---- INSCRIPCION (tabla asociativa Socio ↔ Actividad, resuelve N:M) -------
CREATE TABLE inscripcion (
  id_inscripcion    INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_socio          INT UNSIGNED NOT NULL,
  id_actividad      INT UNSIGNED NOT NULL,
  fecha_inscripcion DATE NOT NULL,
  estado            ENUM('activa','baja') NOT NULL DEFAULT 'activa',
  PRIMARY KEY (id_inscripcion),
  UNIQUE KEY uq_socio_actividad (id_socio, id_actividad),
  CONSTRAINT fk_inscripcion_socio
    FOREIGN KEY (id_socio) REFERENCES socio (id_socio)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_inscripcion_actividad
    FOREIGN KEY (id_actividad) REFERENCES actividad (id_actividad)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ---- PAGO (FK → socio, FK → actividad) ------------------------------------
CREATE TABLE pago (
  id_pago      INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_socio     INT UNSIGNED NOT NULL,
  id_actividad INT UNSIGNED NOT NULL,
  fecha_pago   DATE NOT NULL,
  monto        DECIMAL(10,2) NOT NULL,
  metodo_pago  ENUM('efectivo','debito','credito') NOT NULL,
  PRIMARY KEY (id_pago),
  CONSTRAINT fk_pago_socio
    FOREIGN KEY (id_socio) REFERENCES socio (id_socio)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_pago_actividad
    FOREIGN KEY (id_actividad) REFERENCES actividad (id_actividad)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ---- ASISTENCIA (FK → inscripcion) ----------------------------------------
CREATE TABLE asistencia (
  id_asistencia  INT UNSIGNED NOT NULL AUTO_INCREMENT,
  id_inscripcion INT UNSIGNED NOT NULL,
  fecha          DATE NOT NULL,
  presente       TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (id_asistencia),
  UNIQUE KEY uq_inscripcion_fecha (id_inscripcion, fecha),
  CONSTRAINT fk_asistencia_inscripcion
    FOREIGN KEY (id_inscripcion) REFERENCES inscripcion (id_inscripcion)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ============================================================================
--  SECCIÓN 2 — VISTAS POR ROL (nivel de vistas)
--  2a: vista pública para el socio (no ve el desglose interno).
--  2b: vista gerencial (dashboard de ingresos).
--  2c: vista de clases con cupo disponible (recepcionista / consultas).
--  Se crean ANTES del DCL para poder otorgar permisos sobre ellas.
-- ============================================================================

CREATE OR REPLACE VIEW vista_mis_datos AS
SELECT s.nombre,
       s.apellido,
       i.id_actividad,
       a.nombre        AS nombre_actividad,
       i.estado,
       i.fecha_inscripcion
FROM socio s
JOIN inscripcion i ON i.id_socio = s.id_socio
JOIN actividad  a  ON a.id_actividad = i.id_actividad
WHERE s.activo = 1;

CREATE OR REPLACE VIEW vista_ingresos_mensuales AS
SELECT YEAR(p.fecha_pago)     AS anio,
       MONTH(p.fecha_pago)    AS mes,
       COUNT(p.id_pago)       AS cantidad_pagos,
       ROUND(SUM(p.monto), 2) AS total_facturado
FROM pago p
GROUP BY YEAR(p.fecha_pago), MONTH(p.fecha_pago);

CREATE OR REPLACE VIEW vista_clases_disponibles AS
SELECT a.id_actividad,
       a.nombre,
       a.cupo_maximo,
       COUNT(i.id_inscripcion)                   AS inscriptos,
       (a.cupo_maximo - COUNT(i.id_inscripcion)) AS cupos_libres,
       CONCAT(pr.nombre, ' ', pr.apellido)       AS profesor
FROM actividad a
LEFT JOIN inscripcion i ON i.id_actividad = a.id_actividad AND i.estado = 'activa'
LEFT JOIN profesor pr   ON pr.id_profesor = a.id_profesor
GROUP BY a.id_actividad, a.nombre, a.cupo_maximo, pr.nombre, pr.apellido;

-- ============================================================================
--  SECCIÓN 3 — DCL: USUARIOS Y PERMISOS (cuentas creadas manualmente)
--  Roles heredados del parcial 1: recepcionista, profesor, gerente, socio.
--  Nota: el host 'localhost' limita las conexiones a la máquina local.
-- ============================================================================

CREATE USER IF NOT EXISTS 'recepcionista'@'localhost' IDENTIFIED BY 'Recep2026!';
CREATE USER IF NOT EXISTS 'profesor'@'localhost'      IDENTIFIED BY 'Profe2026!';
CREATE USER IF NOT EXISTS 'gerente'@'localhost'       IDENTIFIED BY 'Gerente2026!';
CREATE USER IF NOT EXISTS 'socio'@'localhost'         IDENTIFIED BY 'Socio2026!';

-- Recepcionista: CRUD sobre socio y pago, sin datos financieros agregados.
GRANT SELECT, INSERT, UPDATE ON gimnasio.socio TO 'recepcionista'@'localhost';
GRANT SELECT, INSERT, UPDATE ON gimnasio.pago  TO 'recepcionista'@'localhost';

-- Profesor: asistencia completa + lectura restringida del socio (solo contacto)
-- y puede actualizar el monto de la actividad que dicta.
GRANT SELECT, INSERT, UPDATE ON gimnasio.asistencia TO 'profesor'@'localhost';
GRANT SELECT (id_socio, nombre, apellido) ON gimnasio.socio TO 'profesor'@'localhost';
GRANT UPDATE (monto) ON gimnasio.actividad TO 'profesor'@'localhost';

-- Gerente: solo lectura de todo (tablas normalizadas) + vistas de dashboard.
GRANT SELECT ON gimnasio.* TO 'gerente'@'localhost';

-- Socio: nivel público, solo ve su propia vista.
GRANT SELECT ON gimnasio.vista_mis_datos TO 'socio'@'localhost';

FLUSH PRIVILEGES;

-- ============================================================================
--  SECCIÓN 4 — DML: CARGA DE DATOS
--  Se popula la base ANTES de hacer las consultas desde Python (rúbrica).
-- ============================================================================

INSERT INTO profesor (nombre, apellido, especialidad, salario) VALUES
  ('Marcela', 'Videla',     'Powerlifting', 850000.00),
  ('Jorge',   'Antonietta', 'CrossFit',     800000.00),
  ('Laura',   'Ponce',      'Yoga',         700000.00),
  ('Diego',   'Sarmiento',  'Boxeo',        760000.00);

INSERT INTO socio (nombre, apellido, dni, email, fecha_alta, activo) VALUES
  ('Ana',      'Concina',  '41234567', 'ana.concina@mail.com',     '2025-03-01', 1),
  ('Bruno',    'Di Paola', '40555123', 'bruno.dipaola@mail.com',   '2025-04-15', 1),
  ('Carla',    'Nieva',    '43777890', 'carla.nieva@mail.com',     '2025-06-20', 1),
  ('Daniela',  'Rojas',    '27890123', 'daniela.rojas@mail.com',   '2025-07-10', 1),
  ('Esteban',  'Peralta',  '32223456', 'esteban.peralta@mail.com', '2025-08-05', 1),
  ('Federico', 'Quintero', '39111222', 'fede.quintero@mail.com',   '2025-09-12', 0);

INSERT INTO actividad (nombre, cupo_maximo, monto, id_profesor) VALUES
  ('CrossFit WOD',      20, 22000.00, 2),
  ('Yoga-Restaurativa', 15, 18000.00, 3),
  ('Powerlifting Club', 12, 25000.00, 1),
  ('Boxeo Amateur',     18, 20000.00, 4);

INSERT INTO inscripcion (id_socio, id_actividad, fecha_inscripcion, estado) VALUES
  (1, 1, '2025-04-01', 'activa'),
  (1, 3, '2025-04-01', 'activa'),
  (2, 1, '2025-05-02', 'activa'),
  (2, 2, '2025-05-02', 'baja'),
  (3, 2, '2025-06-21', 'activa'),
  (3, 4, '2025-06-21', 'activa'),
  (4, 1, '2025-07-15', 'activa'),
  (5, 4, '2025-08-10', 'activa'),
  (6, 3, '2025-09-14', 'baja');

INSERT INTO pago (id_socio, id_actividad, fecha_pago, monto, metodo_pago) VALUES
  (1, 1, '2025-04-01', 22000.00, 'debito'),
  (1, 3, '2025-04-01', 25000.00, 'credito'),
  (2, 1, '2025-05-02', 22000.00, 'efectivo'),
  (3, 2, '2025-06-21', 18000.00, 'debito'),
  (4, 1, '2025-07-15', 22000.00, 'credito'),
  (5, 4, '2025-08-10', 20000.00, 'efectivo'),
  (6, 3, '2025-09-14', 25000.00, 'debito');

INSERT INTO asistencia (id_inscripcion, fecha, presente) VALUES
  (1, '2025-04-03', 1), (1, '2025-04-05', 1), (1, '2025-04-08', 0),
  (3, '2025-05-05', 1), (3, '2025-05-07', 1),
  (5, '2025-06-23', 1), (5, '2025-06-25', 0),
  (7, '2025-07-17', 1);

-- ============================================================================
--  SECCIÓN 5 — TRANSACCIONES (COMMIT y ROLLBACK)
-- ============================================================================

-- 5.1 Transacción CONFIRMADA: alta de inscripción + pago asociado.
--     Si el pago fallara (por ejemplo monto inválido), se deshace TODO.
START TRANSACTION;

INSERT INTO inscripcion (id_socio, id_actividad, fecha_inscripcion, estado)
VALUES (2, 3, '2026-10-26', 'activa');

INSERT INTO pago (id_socio, id_actividad, fecha_pago, monto, metodo_pago)
VALUES (2, 3, '2026-10-26', 25000.00, 'debito');

COMMIT;

-- 5.2 Transacción RECHAZADA (ROLLBACK): borrado accidental de pagos de un socio.
--     Se ejecuta el DELETE, se comprueba el estado, y se deshace.
START TRANSACTION;

DELETE FROM pago
WHERE id_socio = 5;

SELECT COUNT(*) AS pagos_que_quedarian FROM pago WHERE id_socio = 5;

ROLLBACK;

-- Verificación: el socio 5 conserva su pago (el DELETE fue deshecho).
SELECT COUNT(*) AS pagos_actuales FROM pago WHERE id_socio = 5;

-- ============================================================================
--  SECCIÓN 6 — DML AVANZADO CON FUNCIONES NATIVAS
-- ============================================================================

-- 6.1 UPDATE con subconsulta: sube 10% el monto solo de actividades que
--     tienen al menos una inscripción activa (funciones ROUND + IN subquery).
UPDATE actividad
SET monto = ROUND(monto * 1.10, 2)
WHERE id_actividad IN (SELECT DISTINCT id_actividad
                       FROM inscripcion
                       WHERE estado = 'activa');

-- 6.2 UPDATE con funciones de fecha: baja automática de inscripciones viejas.
UPDATE inscripcion
SET estado = 'baja'
WHERE fecha_inscripcion < DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
  AND estado = 'activa';

-- 6.3 DELETE con función nativa: limpieza de asistencias de más de un año.
DELETE FROM asistencia
WHERE YEAR(fecha) < YEAR(CURDATE()) - 1;

-- 6.4 INSERT masivo con funciones: pre-registrar la asistencia de HOY
--     para cada inscripción activa (INSERT ... SELECT + NOT EXISTS).
INSERT INTO asistencia (id_inscripcion, fecha, presente)
SELECT i.id_inscripcion, CURDATE(), 0
FROM inscripcion i
WHERE i.estado = 'activa'
  AND NOT EXISTS (SELECT 1 FROM asistencia a
                  WHERE a.id_inscripcion = i.id_inscripcion
                    AND a.fecha = CURDATE());

-- ============================================================================
--  SECCIÓN 7 — CONSULTAS COMPLEJAS
--  Rúbrica: JOIN + GROUP BY + LIKE con comodines + subconsulta.
-- ============================================================================

-- 7.1 JOIN de 3 tablas + GROUP BY + HAVING:
--     recaudación por actividad (solo las que tienen pago registrado).
SELECT a.nombre                              AS actividad,
       CONCAT(pr.apellido, ', ', pr.nombre)  AS profesor,
       COUNT(DISTINCT i.id_inscripcion)      AS inscriptos,
       COUNT(DISTINCT pa.id_pago)            AS cant_pagos,
       ROUND(SUM(pa.monto), 2)               AS recaudado
FROM actividad a
LEFT JOIN profesor    pr ON pr.id_profesor  = a.id_profesor
LEFT JOIN inscripcion i  ON i.id_actividad  = a.id_actividad
LEFT JOIN pago        pa ON pa.id_socio     = i.id_socio
                        AND pa.id_actividad = a.id_actividad
GROUP BY a.id_actividad
HAVING cant_pagos >= 1
ORDER BY recaudado DESC;

-- 7.2 LIKE con comodines: apellidos que empiezan con 'N' (comodín %)
--     y nombres con 'a' en la 2ª posición (comodín _).
SELECT nombre, apellido, email
FROM socio
WHERE apellido LIKE 'N%'
   OR nombre    LIKE '_a%';

-- 7.3 Subconsulta anidada: socios que pagaron más que el promedio total.
SELECT nombre, apellido
FROM socio s
WHERE (SELECT COALESCE(SUM(pg.monto), 0)
       FROM pago pg
       WHERE pg.id_socio = s.id_socio) >
      (SELECT AVG(total) FROM
        (SELECT SUM(monto) AS total FROM pago GROUP BY id_socio) t);

-- 7.4 Subconsulta en WHERE: actividades sin inscriptos activos.
SELECT nombre, cupo_maximo
FROM actividad
WHERE id_actividad NOT IN (
    SELECT id_actividad FROM inscripcion WHERE estado = 'activa'
);

-- 7.5 Consulta al nivel de vistas: qué ve el rol SOCIO.
SELECT * FROM vista_mis_datos WHERE apellido = 'Concina';
