# 🚀 Quick Start - Deployment en 3 Pasos

## Paso 1: Prepara el Servidor

```bash
# Asegúrate de tener Docker instalado
docker --version
docker-compose --version

# Si no están instalados:
sudo apt update
sudo apt install docker.io docker-compose -y
```

## Paso 2: Copia el Proyecto

```bash
# Navega al directorio del proyecto
cd /home/dreiko98/Escritorio/auto_thumbnail

# O clona desde Git si está en un repositorio:
# git clone <tu-repo-url>
# cd auto_thumbnail
```

## Paso 3: Deploy Automático

```bash
# Ejecuta el script de deployment
./deploy_production.sh
```

**¡Eso es todo!** 🎉

---

## Acceso a la Aplicación

Después del deployment:

- **Aplicación:** http://localhost:5000
- **Nginx:** http://localhost:8080
- **Para acceso externo:** Configura tu dominio para apuntar al servidor

---

## ¿Qué incluye este deployment?

✅ Autenticación de usuarios (registro/login)
✅ Cambio de contraseña
✅ Gestión de tokens OpenAI
✅ Generación de thumbnails
✅ Generación con IA (DALL-E 3)
✅ Exportación de prompts (gratis)
✅ Limpieza automática de archivos
✅ Persistencia de base de datos
✅ Health checks
✅ Restart automático

---

## Comandos Útiles

### Ver Logs
```bash
docker-compose logs -f
```

### Reiniciar
```bash
docker-compose restart
```

### Detener
```bash
docker-compose down
```

### Actualizar
```bash
docker-compose down
# Actualiza código (git pull, etc.)
./deploy_production.sh
```

---

## Verificar que Todo Funciona

```bash
# Health check
curl http://localhost:5000/health

# Debería mostrar:
# {"status":"ok","message":"Thumbnail Generator Web App funcionando correctamente"}
```

---

## ¿Problemas?

Consulta la guía completa: `DEPLOYMENT_GUIDE.md`

O revisa los logs:
```bash
docker-compose logs app
```

---

**¡Disfruta tu Thumbnail Generator!** 🎨✨
