-- ════════════════════════════════════════════════════════════
--  TecnoSoporte SAC – Script de Base de Datos
--  Ejecutar en EC2-DB como usuario root de MySQL
-- ════════════════════════════════════════════════════════════

-- 1. Crear base de datos
CREATE DATABASE IF NOT EXISTS soporte_tecnico
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE soporte_tecnico;

-- 2. Crear tabla tickets
CREATE TABLE IF NOT EXISTS tickets (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    cliente         VARCHAR(100)  NOT NULL,
    telefono        VARCHAR(20)   NOT NULL,
    problema        TEXT          NOT NULL,
    estado          ENUM('Pendiente','En Proceso','Resuelto') NOT NULL DEFAULT 'Pendiente',
    fecha_registro  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Crear usuario de aplicación
--    Reemplaza 'IP_PRIVADA_EC2_WEB' por la IP privada real de tu instancia EC2-WEB
CREATE USER IF NOT EXISTS 'app_user'@'IP_PRIVADA_EC2_WEB'
  IDENTIFIED BY 'AppPassword123!';

-- 4. Otorgar permisos solo sobre la BD del proyecto
GRANT SELECT, INSERT, UPDATE, DELETE
  ON soporte_tecnico.*
  TO 'app_user'@'IP_PRIVADA_EC2_WEB';

FLUSH PRIVILEGES;

-- 5. Datos de prueba (opcional)
INSERT INTO tickets (cliente, telefono, problema, estado) VALUES
  ('María García',    '999-111-222', 'La impresora no imprime en color.',      'Pendiente'),
  ('Carlos López',    '999-333-444', 'No puedo acceder a mi correo corporativo.', 'En Proceso'),
  ('Ana Rodríguez',   '999-555-666', 'Pantalla azul al iniciar Windows.',      'Resuelto');

-- Verificar
SELECT * FROM tickets;
