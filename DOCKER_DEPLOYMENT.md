# 🐳 Guía de Deployment con Docker

## Cambios Necesarios para Docker

### 1. Actualizar `Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar archivos de la aplicación
COPY generate_thumbnail.py .
COPY web_app.py .
COPY wsgi.py .
COPY database.py .
COPY ai_generator.py .
COPY init_db.py .
COPY static/ ./static/
COPY templates/ ./templates/

# Crear carpetas necesarias
RUN mkdir -p .uploads

# Inicializar base de datos
RUN python3 init_db.py

# Exponer puerto
EXPOSE 5000

# Comando por defecto
CMD ["python3", "web_app.py"]
```

### 2. Actualizar `docker-compose.yml`

```yaml
version: '3.8'

services:
  thumbnail-generator:
    build: .
    container_name: thumbnail-generator
    ports:
      - "5000:5000"
    volumes:
      # Persistir base de datos
      - ./data/thumbnail_users.db:/app/thumbnail_users.db
      # Persistir imágenes generadas
      - ./data/uploads:/app/.uploads
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY:-your-secret-key-change-this}
    restart: unless-stopped
    networks:
      - thumbnail-network

networks:
  thumbnail-network:
    driver: bridge
```

### 3. Crear carpetas de datos

```bash
mkdir -p data/uploads
```

### 4. Variables de Entorno (Opcional)

Crear archivo `.env` en el directorio raíz:

```env
SECRET_KEY=tu-clave-secreta-super-segura-cambiala
FLASK_ENV=production
```

---

## 📋 Paso a Paso para Deployment

### Opción A: Deployment Local con Docker

```bash
# 1. Detener contenedor actual (si existe)
docker-compose down

# 2. Hacer backup de la base de datos (si existe)
cp thumbnail_users.db data/thumbnail_users.db.backup

# 3. Rebuild con nuevos cambios
docker-compose build --no-cache

# 4. Iniciar contenedor
docker-compose up -d

# 5. Ver logs
docker-compose logs -f
```

### Opción B: Deployment en Servidor Remoto

```bash
# 1. Conectar al servidor
ssh usuario@tu-servidor.com

# 2. Navegar al directorio del proyecto
cd /ruta/a/auto_thumbnail

# 3. Hacer backup
docker-compose down
cp thumbnail_users.db data/thumbnail_users.db.backup

# 4. Pull últimos cambios (si usas git)
git pull origin main

# 5. Rebuild y reiniciar
docker-compose build --no-cache
docker-compose up -d

# 6. Verificar que funciona
docker-compose ps
docker-compose logs -f thumbnail-generator
```

### Opción C: Deployment con script automatizado

Crear archivo `deploy_docker_ai.sh`:

```bash
#!/bin/bash

echo "🚀 Deploying Thumbnail Generator con IA..."

# Detener servicios
echo "⏸️  Deteniendo servicios..."
docker-compose down

# Backup
echo "💾 Haciendo backup..."
mkdir -p backups
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
if [ -f "data/thumbnail_users.db" ]; then
    cp data/thumbnail_users.db "backups/thumbnail_users_${TIMESTAMP}.db"
    echo "  ✓ Backup: backups/thumbnail_users_${TIMESTAMP}.db"
fi

# Crear carpetas necesarias
echo "📁 Creando carpetas..."
mkdir -p data/uploads

# Build nueva imagen
echo "🔨 Building imagen Docker..."
docker-compose build --no-cache

if [ $? -eq 0 ]; then
    echo "  ✓ Build exitoso"
else
    echo "  ✗ Error en build"
    exit 1
fi

# Iniciar servicios
echo "▶️  Iniciando servicios..."
docker-compose up -d

if [ $? -eq 0 ]; then
    echo "  ✓ Servicios iniciados"
else
    echo "  ✗ Error al iniciar"
    exit 1
fi

# Verificar estado
echo "🔍 Verificando estado..."
sleep 3
docker-compose ps

echo ""
echo "================================================"
echo "✅ Deployment completado"
echo "================================================"
echo ""
echo "📊 Para ver logs:"
echo "   docker-compose logs -f"
echo ""
echo "🌐 La aplicación debería estar disponible en:"
echo "   http://localhost:5000"
echo "   o tu dominio configurado"
echo ""
```

Hacer ejecutable:
```bash
chmod +x deploy_docker_ai.sh
```

---

## 🔧 Configuración de Nginx (Si usas proxy reverso)

Actualizar `nginx.conf` o `nginx.docker.conf`:

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    # Aumentar límites para uploads
    client_max_body_size 50M;

    # Aumentar timeout para generación con IA
    proxy_connect_timeout 120;
    proxy_send_timeout 120;
    proxy_read_timeout 120;

    location / {
        proxy_pass http://thumbnail-generator:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /app/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

**Importante**: El timeout de 120 segundos es necesario porque la generación con IA puede tomar 10-30 segundos.

---

## 📊 Monitoreo

### Ver logs en tiempo real
```bash
docker-compose logs -f thumbnail-generator
```

### Ver estado de contenedores
```bash
docker-compose ps
```

### Verificar uso de recursos
```bash
docker stats thumbnail-generator
```

### Ver base de datos
```bash
docker exec -it thumbnail-generator sqlite3 thumbnail_users.db
sqlite> SELECT username, openai_token IS NOT NULL as has_token, created_at FROM users;
sqlite> .quit
```

---

## 🐛 Troubleshooting Docker

### Error: "Cannot connect to Docker daemon"
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### Error: "Port 5000 already in use"
```bash
# Ver qué está usando el puerto
sudo lsof -i :5000

# O cambiar el puerto en docker-compose.yml
ports:
  - "5001:5000"  # Usar 5001 en lugar de 5000
```

### Error: "Database is locked"
```bash
# Detener contenedor
docker-compose down

# Verificar que no hay procesos usando la DB
lsof | grep thumbnail_users.db

# Reiniciar
docker-compose up -d
```

### Rebuild completo (limpia todo)
```bash
docker-compose down -v
docker system prune -a
docker-compose build --no-cache
docker-compose up -d
```

---

## 🔐 Seguridad

### 1. Cambiar SECRET_KEY
```bash
# Generar nueva clave
python3 -c "import secrets; print(secrets.token_hex(32))"

# Agregar a .env
echo "SECRET_KEY=tu-nueva-clave-aqui" > .env
```

### 2. Proteger tokens OpenAI
- Los tokens se guardan encriptados en la base de datos
- **NUNCA** exponer `thumbnail_users.db` públicamente
- Hacer backups regulares y seguros

### 3. HTTPS
```bash
# Si usas Let's Encrypt con Certbot
sudo certbot --nginx -d tu-dominio.com
```

### 4. Limitar acceso
```nginx
# En nginx.conf, permitir solo IPs específicas
location /register {
    allow 192.168.1.0/24;
    deny all;
    proxy_pass http://thumbnail-generator:5000;
}
```

---

## 📦 Backup y Restore

### Backup automático
Crear script `backup_db.sh`:

```bash
#!/bin/bash
BACKUP_DIR="backups"
mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Backup DB
cp data/thumbnail_users.db "$BACKUP_DIR/db_${TIMESTAMP}.db"

# Backup uploads
tar -czf "$BACKUP_DIR/uploads_${TIMESTAMP}.tar.gz" data/uploads/

# Limpiar backups viejos (más de 7 días)
find "$BACKUP_DIR" -name "*.db" -mtime +7 -delete
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete

echo "Backup completado: ${TIMESTAMP}"
```

Agregar a crontab para ejecutar diariamente:
```bash
crontab -e
# Agregar:
0 2 * * * /ruta/a/auto_thumbnail/backup_db.sh
```

### Restore desde backup
```bash
# Detener servicios
docker-compose down

# Restore DB
cp backups/db_20240115_020000.db data/thumbnail_users.db

# Restore uploads
tar -xzf backups/uploads_20240115_020000.tar.gz -C data/

# Reiniciar
docker-compose up -d
```

---

## 📈 Optimizaciones

### 1. Usar imágenes más ligeras
```dockerfile
FROM python:3.11-alpine  # En lugar de slim

RUN apk add --no-cache \
    gcc \
    g++ \
    jpeg-dev \
    zlib-dev
```

### 2. Cache de pip
```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

### 3. Multi-stage build
```dockerfile
# Stage 1: Build
FROM python:3.11 as builder
# ... instalación de dependencias

# Stage 2: Runtime
FROM python:3.11-slim
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
# ... resto de archivos
```

---

## ✅ Checklist de Deployment

- [ ] Actualizar `Dockerfile` con nuevos archivos
- [ ] Actualizar `docker-compose.yml` con volúmenes
- [ ] Crear carpeta `data/uploads`
- [ ] Configurar SECRET_KEY en `.env`
- [ ] Hacer backup de DB existente
- [ ] Build imagen: `docker-compose build --no-cache`
- [ ] Iniciar: `docker-compose up -d`
- [ ] Verificar logs: `docker-compose logs -f`
- [ ] Probar registro de usuario
- [ ] Probar configuración de token OpenAI
- [ ] Probar generación de imagen con IA
- [ ] Verificar que imagen se usa en thumbnail
- [ ] Configurar nginx con timeouts largos (si aplica)
- [ ] Configurar HTTPS (si aplica)
- [ ] Configurar backups automáticos

---

## 🆘 Soporte

Si encuentras problemas:

1. **Ver logs detallados**:
   ```bash
   docker-compose logs -f thumbnail-generator
   ```

2. **Entrar al contenedor**:
   ```bash
   docker exec -it thumbnail-generator bash
   ```

3. **Verificar archivos**:
   ```bash
   docker exec thumbnail-generator ls -la
   docker exec thumbnail-generator ls -la data/
   ```

4. **Probar manualmente**:
   ```bash
   docker exec -it thumbnail-generator python3
   >>> import database
   >>> database.init_database()
   >>> import ai_generator
   >>> # Probar funciones
   ```

5. **Rebuild desde cero**:
   ```bash
   docker-compose down -v
   docker system prune -a -f
   docker-compose up --build
   ```
