# 🚀 Guía de Deployment - Thumbnail Generator

## 📋 Resumen de Características Implementadas

### ✅ Autenticación y Gestión de Usuarios
- ✅ Sistema completo de registro/login
- ✅ Gestión de sesiones seguras
- ✅ Almacenamiento de tokens OpenAI por usuario
- ✅ **NUEVO:** Cambio de contraseña
- ✅ **NUEVO:** Cambio de API key cuando sea necesario
- ✅ Hash SHA-256 con salt único por usuario

### ✅ Gestión de Archivos
- ✅ **NO se guarda ningún archivo permanentemente**
- ✅ Limpieza automática después de generar thumbnails
- ✅ Limpieza al iniciar el servidor
- ✅ Limpieza al detener el servidor
- ✅ Solo se persiste la base de datos de usuarios
- ✅ Carpeta `/static` intacta (avatares, favicon, etc.)

### ✅ Features de IA
- ✅ Generación de fondos con DALL-E 3
- ✅ Generación de iconos transparentes
- ✅ Exportación de prompts optimizados (sin costo)
- ✅ Cada usuario usa su propio token OpenAI

---

## 🐳 Deployment con Docker

### 1. Requisitos Previos

```bash
# Verificar que Docker está instalado
docker --version
docker-compose --version

# Si no están instalados:
# sudo apt update
# sudo apt install docker.io docker-compose
```

### 2. Preparar el Proyecto

```bash
# Navegar al directorio del proyecto
cd /home/dreiko98/Escritorio/auto_thumbnail

# El script de deployment se encarga del resto
./deploy_production.sh
```

### 3. ¿Qué hace el script?

El script `deploy_production.sh` realiza automáticamente:

1. ✅ Verifica que estés en el directorio correcto
2. ✅ Crea archivo `.env` con clave secreta única (si no existe)
3. ✅ Detiene contenedores existentes
4. ✅ Construye imágenes Docker nuevas
5. ✅ Inicia los servicios
6. ✅ Verifica que todo esté funcionando (health check)
7. ✅ Muestra información de acceso

### 4. Acceso a la Aplicación

Después del deployment:

- **Aplicación directa:** http://localhost:5000
- **A través de Nginx:** http://localhost:8080

Para acceso desde internet (con tu dominio):
- Configura tu dominio para apuntar al servidor
- Nginx reverse proxy ya está configurado

---

## 🗄️ Base de Datos

### Persistencia

La base de datos se almacena en un **Docker volume** persistente:

```yaml
volumes:
  thumbnail_db:
    driver: local
```

Esto significa que:
- ✅ Los usuarios se mantienen entre reinicios
- ✅ Las contraseñas persisten
- ✅ Los tokens OpenAI se guardan
- ✅ Puedes actualizar el contenedor sin perder datos

### Backup de la Base de Datos

```bash
# Exportar la base de datos
docker run --rm \
  -v thumbnail_db:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/thumbnail_db_backup.tar.gz -C /data .

# Restaurar backup
docker run --rm \
  -v thumbnail_db:/data \
  -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/thumbnail_db_backup.tar.gz"
```

---

## 🗑️ Gestión de Archivos Temporales

### Política de Limpieza

**IMPORTANTE:** Esta aplicación NO guarda archivos de usuarios permanentemente.

#### Archivos que se eliminan automáticamente:

1. **Imágenes subidas por usuarios**
   - Imagen de fondo
   - Iconos
   - Fotos de personas

2. **Imágenes generadas por IA**
   - Fondos generados con DALL-E
   - Iconos generados con IA

3. **Thumbnails resultantes**
   - Se eliminan después de enviar al usuario como base64

#### Momentos de limpieza:

- ✅ **Inmediatamente después de generar** el thumbnail
- ✅ **Al iniciar** el servidor (limpia todo lo que quedó)
- ✅ **Al detener** el servidor (limpieza final)
- ✅ **Periódicamente** (archivos > 1 hora de antigüedad)

#### Archivos que SÍ se mantienen:

- ✅ `/static/avatar.png`
- ✅ `/static/avatar2.png`
- ✅ `/static/favicon.ico`
- ✅ Base de datos `thumbnail_users.db` (en volumen Docker)

### Verificar Limpieza

```bash
# Ver archivos temporales (debería estar vacío o casi vacío)
docker exec thumbnail-app ls -la /app/.uploads
docker exec thumbnail-app ls -la /app/.results

# Ver logs de limpieza
docker-compose logs app | grep "🗑️"
```

---

## 🔐 Seguridad

### Variables de Entorno

El archivo `.env` contiene configuración sensible:

```bash
# .env (generado automáticamente)
FLASK_SECRET_KEY=<clave_única_de_64_caracteres>
DATABASE_PATH=/app/db_data/thumbnail_users.db
```

**NUNCA** subas `.env` a Git.

### Contraseñas

- Hash SHA-256 con salt único por usuario
- Salt de 64 caracteres hexadecimales
- No se almacenan contraseñas en texto plano

### Tokens OpenAI

- Cada usuario almacena su propio token
- Se pueden actualizar en cualquier momento
- Se pueden eliminar si el usuario ya no quiere usarlos

---

## 📊 Monitoreo

### Ver Logs en Tiempo Real

```bash
# Todos los servicios
docker-compose logs -f

# Solo la aplicación
docker-compose logs -f app

# Solo Nginx
docker-compose logs -f nginx

# Últimas 100 líneas
docker-compose logs --tail 100 app
```

### Health Check

```bash
# Verificar que la aplicación está corriendo
curl http://localhost:5000/health

# Debería devolver:
# {"status":"ok","message":"Thumbnail Generator Web App funcionando correctamente"}
```

### Estado de Contenedores

```bash
# Ver contenedores activos
docker-compose ps

# Deberías ver:
# thumbnail-app   running
# thumbnail-nginx running
```

---

## 🔄 Actualizar la Aplicación

### Actualización Simple

```bash
# Detener servicios
docker-compose down

# Actualizar código (git pull, etc.)
git pull origin main

# Reconstruir y reiniciar
./deploy_production.sh
```

### Actualización sin Perder Datos

```bash
# El volumen de la base de datos NO se elimina con docker-compose down
# Por lo tanto, tus usuarios y configuraciones persisten

# Para limpiar TODO (incluyendo base de datos):
# ⚠️ CUIDADO: Esto eliminará todos los usuarios
docker-compose down -v  # El flag -v elimina volúmenes
```

---

## 🛠️ Comandos Útiles

### Gestión de Contenedores

```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Reconstruir imágenes
docker-compose build --no-cache

# Ver estado
docker-compose ps

# Ver uso de recursos
docker stats thumbnail-app
```

### Acceso al Contenedor

```bash
# Shell interactivo
docker exec -it thumbnail-app /bin/bash

# Ejecutar comando único
docker exec thumbnail-app ls -la /app

# Ver archivos de base de datos
docker exec thumbnail-app ls -la /app/db_data
```

### Limpieza de Docker

```bash
# Limpiar imágenes no usadas
docker image prune -a

# Limpiar todo (contenedores, imágenes, volúmenes)
# ⚠️ CUIDADO: Esto eliminará TODA la base de datos
docker system prune -a --volumes
```

---

## 🐛 Troubleshooting

### Problema: La aplicación no inicia

```bash
# Ver logs de error
docker-compose logs app

# Verificar que el puerto 5000 no está en uso
sudo lsof -i :5000

# Si está en uso, matar el proceso o cambiar puerto en docker-compose.yml
```

### Problema: No puedo registrar usuarios

```bash
# Verificar que la base de datos se está creando
docker exec thumbnail-app ls -la /app/db_data/

# Ver logs de base de datos
docker-compose logs app | grep "database\|usuario\|user"

# Conectar a la base de datos y verificar
docker exec -it thumbnail-app sqlite3 /app/db_data/thumbnail_users.db "SELECT * FROM users;"
```

### Problema: Los archivos no se eliminan

```bash
# Verificar función de limpieza
docker-compose logs app | grep "Eliminado\|🗑️"

# Ver archivos temporales actuales
docker exec thumbnail-app find /app/.uploads -type f
docker exec thumbnail-app find /app/.results -type f

# Forzar limpieza manual
docker exec thumbnail-app sh -c "rm -rf /app/.uploads/* /app/.results/*"
```

### Problema: Error de permisos

```bash
# Verificar permisos del directorio de base de datos
docker exec thumbnail-app ls -la /app/db_data

# Arreglar permisos si es necesario
docker exec thumbnail-app chmod 755 /app/db_data
docker exec thumbnail-app chmod 644 /app/db_data/thumbnail_users.db
```

---

## 📝 Notas Adicionales

### Capacidad de la Base de Datos

SQLite puede manejar miles de usuarios sin problemas. Si llegas a necesitar más rendimiento:
- Considera migrar a PostgreSQL
- O usar SQLite en modo WAL (Write-Ahead Logging)

### Límites de OpenAI

Cada usuario usa su propio token, por lo que:
- ✅ Los límites son individuales
- ✅ No compartes costos con otros usuarios
- ✅ Cada usuario controla su propio gasto

### Costos Aproximados

- **Generar fondo (1920x1080):** ~$0.04 USD
- **Generar icono (1024x1024):** ~$0.04 USD
- **Obtener prompt (sin generar):** GRATIS

---

## 🎉 ¡Listo para Producción!

Tu aplicación está ahora configurada con:
- ✅ Autenticación completa
- ✅ Gestión de usuarios y tokens
- ✅ Cambio de contraseña y API key
- ✅ Limpieza automática de archivos
- ✅ Persistencia solo de datos necesarios
- ✅ Health checks y monitoreo
- ✅ Reverse proxy con Nginx
- ✅ Reinicio automático en caso de fallo

**¡Disfruta de tu Thumbnail Generator!** 🚀
