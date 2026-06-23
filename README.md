# 🎧 TecnoSoporte

Sistema web de gestión de tickets de soporte técnico con diseño **dark mode** en tonos rojo y naranja, desplegado en AWS con arquitectura de dos servidores EC2.

---

## ✨ Diseño

- Fondo oscuro `#0f0f0f` con destellos de luz rojo/naranja
- Navbar con efecto **glassmorphism**
- Fuente moderna **Poppins**
- Cards con efecto translúcido
- Badges de estado con colores: 🟡 Pendiente · 🟠 En Proceso · 🟢 Resuelto
- Botones con gradiente **rojo → naranja**
- Inputs oscuros con borde naranja al hacer foco

---

## 🛠️ Tecnologías

- **Backend:** Python 3 + Flask
- **Base de datos:** MySQL 8
- **Frontend:** HTML + Bootstrap 5 + CSS personalizado + Poppins
- **Infraestructura:** AWS EC2 Ubuntu Server 22.04 LTS

---

## 🏗️ Arquitectura AWS

| Servidor | Nombre  | Servicio   |
|----------|---------|------------|
| EC2-DB   | EC2-DB  | MySQL 8    |
| EC2-WEB  | EC2-WEB | Flask App  |

---

## ⚙️ Funcionalidades

- ✅ Registrar tickets de soporte técnico
- ✅ Consultar listado completo de tickets
- ✅ Actualizar estado: Pendiente / En Proceso / Resuelto
- ✅ Eliminar tickets
- ✅ Panel con contadores por estado

---

## 📁 Estructura del proyecto

```
tecnosoporte/
├── app.py              # Lógica principal Flask (rutas CRUD)
├── requirements.txt    # Dependencias Python
├── setup_db.sql        # Script SQL para EC2-DB
├── DEPLOY.md           # Guía de despliegue en AWS
├── README.md           # Este archivo
└── templates/
    ├── base.html       # Layout dark mode rojo/naranja
    ├── index.html      # Panel principal con estadísticas
    ├── nuevo.html      # Formulario registro de ticket
    └── editar.html     # Actualizar estado del ticket
```

---

## 🚀 Despliegue en EC2-WEB

```bash
# Clonar rama develop
git clone -b develop https://github.com/oscarsanchez0712/tecnosoporte.git
cd tecnosoporte

# Entorno virtual
python3 -m venv venv
source venv/bin/activate

# Dependencias
pip install -r requirements.txt

# Variables de entorno
export DB_HOST="IP_PRIVADA_EC2_DB"
export DB_USER="app_user"
export DB_PASSWORD="AppPassword123!"
export DB_NAME="soporte_tecnico"

# Ejecutar
python3 app.py
```

---

## 🗄️ Base de datos (EC2-DB)

```sql
CREATE DATABASE soporte_tecnico;
USE soporte_tecnico;

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

**Oscar Heyton Sanchez Arias**  
Curso: Despliegue de una Aplicación Web en AWS Cloud  
Docente: Ebert Ocares
