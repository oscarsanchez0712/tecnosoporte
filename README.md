# 🎧 TecnoSoporte SAC

Aplicación web para gestión de tickets de soporte técnico, desplegada en AWS con arquitectura de dos servidores EC2.

---

## 🛠️ Tecnologías

- **Backend:** Python 3 + Flask
- **Base de datos:** MySQL 8
- **Infraestructura:** AWS EC2 (Ubuntu Server 22.04 LTS)
- **Frontend:** HTML, Bootstrap 5, CSS personalizado

---

## 🏗️ Arquitectura

| Servidor | Función | Servicio |
|----------|---------|---------|
| EC2-DB   | Base de datos | MySQL 8 |
| EC2-WEB  | Aplicación web | Flask |

---

## ⚙️ Funcionalidades

- ✅ Registrar tickets de soporte técnico
- ✅ Consultar listado de tickets
- ✅ Actualizar estado: Pendiente / En Proceso / Resuelto
- ✅ Eliminar tickets

---

## 🚀 Instalación local

```bash
# Clonar el repositorio
git clone -b develop https://github.com/oscarsanchez0712/tecnosoporte.git
cd tecnosoporte

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
export DB_HOST="IP_PRIVADA_EC2_DB"
export DB_USER="app_user"
export DB_PASSWORD="AppPassword123!"
export DB_NAME="soporte_tecnico"

# Ejecutar la aplicación
python3 app.py
```

---

## 🗄️ Base de datos

```sql
CREATE DATABASE soporte_tecnico;

CREATE TABLE tickets (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  cliente        VARCHAR(100) NOT NULL,
  telefono       VARCHAR(20)  NOT NULL,
  problema       TEXT         NOT NULL,
  estado         ENUM('Pendiente','En Proceso','Resuelto') DEFAULT 'Pendiente',
  fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 👤 Autor

**Diana Felicitas Huamani Espinoza**  
Curso: Despliegue de una Aplicación Web en AWS Cloud  
Docente: Ebert Ocares
