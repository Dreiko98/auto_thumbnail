# 🎨 Thumbnail Generator · Germán Mallo

Generador profesional de thumbnails de 1920×1080px con sistema de autenticación, integración con IA (DALL-E 3) y despliegue en Docker.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Flask](https://img.shields.io/badge/flask-2.3+-green)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Características Principales

### 🎨 Generación de Thumbnails
- ✅ **3 plantillas profesionales** con diseños modernos
- ✅ Imagen de fondo con desenfoque inteligente
- ✅ Texto personalizable con fuentes modernas
- ✅ Iconos y elementos decorativos
- ✅ Preview en tiempo real

### 🤖 Integración con IA
- ✅ **Generación automática** con DALL-E 3
- ✅ **Fondos optimizados** para thumbnails (1920×1080)
- ✅ **Iconos transparentes** (PNG con alpha channel)
- ✅ **Exportación de prompts** (sin costo de API)
- ✅ Cada usuario usa su propio token OpenAI

### 👤 Sistema de Usuarios
- ✅ Registro y login seguro
- ✅ Contraseñas hasheadas (SHA-256 + salt)
- ✅ Cambio de contraseña
- ✅ Gestión de tokens OpenAI por usuario
- ✅ Base de datos SQLite persistente

### 🗑️ Gestión Inteligente de Archivos
- ✅ **NO se guardan archivos permanentemente**
- ✅ Limpieza automática después de generar
- ✅ Solo se persiste la base de datos
- ✅ Limpieza en startup/shutdown

### 🐳 Docker Production Ready
- ✅ Deployment con un solo comando
- ✅ Nginx reverse proxy incluido
- ✅ Health checks automáticos
- ✅ Volúmenes persistentes para DB
- ✅ Restart automático

---

## 🚀 Quick Start

### Opción 1: Docker (Recomendado)

```bash
# 1. Clonar repositorio
git clone <tu-repo>
cd auto_thumbnail

# 2. Deploy automático
./deploy_production.sh

# 3. Acceder
# http://localhost:5000
```

### Opción 2: Local (Desarrollo)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar aplicación
python3 web_app.py

# 3. Acceder
# http://localhost:5000
```

---

## � Requisitos

Para tener la aplicación ejecutándose 24/7 en tu servidor:

```bash
# 1. Copiar proyecto al servidor
scp -r /ruta/local/auto_thumbnail germanmallo@100.87.242.53:~/auto_thumbnail

# 2. Ejecutar despliegue en el servidor
ssh germanmallo@100.87.242.53
cd auto_thumbnail
chmod +x *.sh
./deploy_server.sh
```

**Resultado:** Tu app estará disponible en `http://100.87.242.53`

#### 🔒 **Configurar SSL (Opcional)**
```bash
./setup_ssl.sh
# Ingresa tu dominio cuando se pregunte
```

#### 📊 **Monitoreo**
```bash
./monitor.sh
```

## ✨ Características

- ✅ **Interfaz Web**: Drag & drop, vista previa
- ✅ **Script CLI**: Uso desde terminal
- ✅ **Redimensionado inteligente**: 1920×1080px con desenfoque
- ✅ **Tipografía profesional**: Fuentes cursivas con efectos
- ✅ **Iconos escalables**: Hasta 4 iconos con sombras
- ✅ **Soporte URLs**: Descarga imágenes remotas
- ✅ **Exportación**: PNG + capas separadas

## 🛠️ Instalación

```bash
# Opción 1: Instalación automática
./install_dependencies.sh

# Opción 2: Manual
pip install -r requirements.txt

# Opción 3: Con entorno virtual (recomendado)
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

## 🚀 Uso

### 🌐 Aplicación Web
```bash
# Inicio rápido
./launch_app.sh

# O manualmente
python3 web_app.py
```
**Acceso:** `http://localhost:5000`

**Características:**
- 🖱️ **Drag & Drop**: Arrastra archivos directamente
- 👁️ **Vista previa**: Ve el resultado antes de descargar
- 📥 **Descarga directa**: Un clic para obtener el PNG

### 💻 Script CLI

**Modo interactivo:**
```bash
python3 generate_thumbnail.py
```

**Con argumentos:**
```bash
python3 generate_thumbnail.py "imagen.jpg" "Mi Título" "icono1.png" "icono2.png"
```

## 🖥️ Despliegue en Producción

### Arquitectura
- **Gunicorn**: Servidor WSGI para Flask
- **Nginx**: Proxy reverso y servidor web
- **Systemd**: Gestión de servicios (auto-inicio)
- **SSL**: Opcional con Let's Encrypt

### Pasos de Despliegue

#### 1. **Preparar el Servidor**
```bash
# Conectar al servidor
ssh germanmallo@100.87.242.53

# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y python3 python3-pip python3-venv nginx gunicorn python3-gunicorn
```

#### 2. **Copiar el Proyecto**
```bash
# Desde tu máquina local
scp -r /home/dreiko98/Escritorio/auto_thumbnail germanmallo@100.87.242.53:~/auto_thumbnail

# O usando git (recomendado)
ssh germanmallo@100.87.242.53
git clone https://github.com/Dreiko98/auto_thumbnail.git
cd auto_thumbnail
```

#### 3. **Configurar la Aplicación**
```bash
# Dar permisos de ejecución
chmod +x *.sh

# Instalar dependencias de Python
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt gunicorn
```

#### 4. **Configurar Servicios del Sistema**

**Servicio Systemd:**
```bash
sudo cp thumbnail-generator.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable thumbnail-generator
```

**Nginx (Proxy Reverso):**
```bash
sudo cp nginx.conf /etc/nginx/sites-available/thumbnail-generator
sudo ln -sf /etc/nginx/sites-available/thumbnail-generator /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default  # Remover configuración por defecto
sudo nginx -t  # Verificar configuración
sudo systemctl reload nginx
```

#### 5. **Iniciar la Aplicación**
```bash
sudo systemctl start thumbnail-generator
sudo systemctl status thumbnail-generator
```

### 🔒 Configurar SSL (HTTPS)

```bash
# Instalar Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tudominio.com

# Verificar renovación automática
sudo certbot renew --dry-run
```

### 📊 Monitoreo y Mantenimiento

```bash
# Ver estado de servicios
sudo systemctl status thumbnail-generator
sudo systemctl status nginx

# Ver logs
sudo journalctl -u thumbnail-generator -f
sudo tail -f /var/log/nginx/thumbnail_access.log

# Reiniciar servicios
sudo systemctl restart thumbnail-generator
sudo systemctl reload nginx

# Uso de script de monitoreo
./monitor.sh
```

### 🌐 URLs de Acceso

- **HTTP**: `http://100.87.242.53`
- **HTTPS** (con SSL): `https://tudominio.com`
- **Health Check**: `http://100.87.242.53/health`

### 🛠️ Solución de Problemas

**Error: Puerto 80 ocupado**
```bash
sudo netstat -tulpn | grep :80
sudo systemctl stop apache2  # Si Apache está ejecutándose
```

**Error: Socket permission denied**
```bash
sudo chown germanmallo:germanmallo /tmp/thumbnail.sock
```

**Error: Nginx no puede conectar**
```bash
sudo systemctl status thumbnail-generator
sudo journalctl -u thumbnail-generator -n 20
```

## 📁 Archivos Generados

- `thumbnail.png` - Imagen final (1920×1080px)
- `thumbnail_capas/` - Capas separadas:
  - `01_fondo_desenfocado.png`
  - `02_texto_info.txt`
  - `03_icono_01.png`, etc.

## ️ Dependencias

- **Python 3.8+**
- **Pillow** (manipulación de imágenes)
- **requests** (descarga de URLs)
- **Flask** (aplicación web)

## 📚 Archivos del Proyecto

```
auto_thumbnail/
├── generate_thumbnail.py     # Motor principal
├── web_app.py               # Aplicación web
├── templates/index.html     # Interfaz web
├── requirements.txt         # Dependencias
├── install_dependencies.sh  # Instalador
├── launch_app.sh           # Lanzador
└── README.md               # Esta guía
```

---

**🎨 ¡Crea thumbnails profesionales en segundos!** 🎨
