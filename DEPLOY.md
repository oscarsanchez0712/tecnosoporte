# 🚀 Guía de Despliegue – TecnoSoporte SAC en AWS

---

## FASE 1 – INFRAESTRUCTURA AWS

### Crear dos instancias EC2 (Ubuntu Server 22.04 LTS)

| Instancia | Nombre  | Función        |
|-----------|---------|----------------|
| EC2-DB    | EC2-DB  | MySQL Database |
| EC2-WEB   | EC2-WEB | Flask Web App  |

### Security Groups

**EC2-WEB-SG**

| Tipo       | Puerto | Origen   |
|------------|--------|----------|
| SSH        | 22     | Mi IP    |
| HTTP       | 80     | Anywhere |
| HTTPS      | 443    | Anywhere |
| Custom TCP | 5000   | Mi IP    |

**EC2-DB-SG**

| Tipo  | Puerto | Origen                   |
|-------|--------|--------------------------|
| SSH   | 22     | Mi IP                    |
| MySQL | 3306   | IP Privada de EC2-WEB    |

> ⚠️ El puerto 3306 NO debe ser público.

---

## FASE 2 – CONFIGURAR EC2-DB (Servidor de Base de Datos)

Conectarse vía SSH:
```bash
ssh -i tu-clave.pem ubuntu@<IP-PUBLICA-EC2-DB>
```

### 1. Actualizar sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Instalar MySQL Server
```bash
sudo apt install mysql-server -y
sudo systemctl start mysql
sudo systemctl enable mysql
```

### 3. Configurar acceso remoto
```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
# Cambiar: bind-address = 127.0.0.1
# Por:     bind-address = 0.0.0.0
sudo systemctl restart mysql
```

### 4. Crear base de datos y usuario
```bash
sudo mysql -u root
```
Dentro de MySQL, ejecutar el contenido de `setup_db.sql`
(reemplazar `IP_PRIVADA_EC2_WEB` por la IP privada real de EC2-WEB).

### 5. Verificar que MySQL escucha en 0.0.0.0
```bash
sudo ss -tlnp | grep 3306
```

---

## FASE 3 – CONFIGURAR EC2-WEB (Servidor de Aplicación)

Conectarse vía SSH:
```bash
ssh -i tu-clave.pem ubuntu@<IP-PUBLICA-EC2-WEB>
```

### 1. Actualizar sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Instalar dependencias del SO
```bash
sudo apt install python3 python3-pip python3-venv git -y
```

### 3. Descargar el proyecto desde GitHub
```bash
git clone https://github.com/TU_USUARIO/TU_REPOSITORIO.git
cd TU_REPOSITORIO
```

### 4. Crear y activar entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Instalar dependencias Python
```bash
pip install -r requirements.txt
```

### 6. Configurar conexión a la base de datos
Edita `app.py` o exporta variables de entorno:
```bash
export DB_HOST="<IP-PRIVADA-EC2-DB>"
export DB_USER="app_user"
export DB_PASSWORD="AppPassword123!"
export DB_NAME="soporte_tecnico"
```

### 7. Verificar conexión a MySQL desde EC2-WEB
```bash
python3 -c "
import mysql.connector
conn = mysql.connector.connect(
    host='<IP-PRIVADA-EC2-DB>',
    user='app_user',
    password='AppPassword123!',
    database='soporte_tecnico'
)
print('✅ Conexión exitosa')
conn.close()
"
```

### 8. Ejecutar la aplicación
```bash
python3 app.py
```
Acceder desde el navegador: `http://<IP-PUBLICA-EC2-WEB>:5000`

---

## FASE 4 – PRUEBAS FUNCIONALES

| Prueba | Acción                                           | Resultado Esperado            |
|--------|--------------------------------------------------|-------------------------------|
| 1      | Registrar nuevo ticket                           | Ticket aparece en el listado  |
| 2      | Consultar listado de tickets                     | Se muestran todos los tickets |
| 3      | Actualizar estado de un ticket a "En Proceso"    | Estado cambia correctamente   |
| 4      | Verificar en MySQL: `SELECT * FROM tickets;`     | Datos almacenados en BD       |
| 5      | Ping de EC2-WEB a EC2-DB por puerto 3306         | Comunicación exitosa          |

### Verificar en MySQL (Prueba 4)
```bash
# Desde EC2-DB
sudo mysql -u root -e "USE soporte_tecnico; SELECT * FROM tickets;"
```

### Verificar comunicación (Prueba 5)
```bash
# Desde EC2-WEB
nc -zv <IP-PRIVADA-EC2-DB> 3306
```

---

## ESTRUCTURA DEL PROYECTO

```
tecnosoporte/
├── app.py              # Aplicación Flask (rutas y lógica)
├── requirements.txt    # Dependencias Python
├── setup_db.sql        # Script SQL (ejecutar en EC2-DB)
├── DEPLOY.md           # Esta guía
└── templates/
    ├── base.html       # Plantilla base (navbar, alerts)
    ├── index.html      # Listado de tickets
    ├── nuevo.html      # Formulario nuevo ticket
    └── editar.html     # Actualizar estado
```
