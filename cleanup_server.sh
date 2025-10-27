#!/bin/bash
# Script de limpieza completa antes de Docker
# Ejecutar en el servidor

echo "🧹 LIMPIANDO DESPLIEGUE ANTERIOR"
echo "================================="

# Detener servicios
echo "🔄 Deteniendo servicios..."
sudo systemctl stop thumbnail-generator 2>/dev/null || echo "Servicio no estaba ejecutándose"
sudo systemctl disable thumbnail-generator 2>/dev/null || echo "Servicio no estaba habilitado"

# Eliminar archivos de configuración
echo "🗑️  Eliminando archivos de configuración..."
sudo rm -f /etc/systemd/system/thumbnail-generator.service
sudo rm -f /etc/nginx/sites-available/thumbnail-generator
sudo rm -f /etc/nginx/sites-enabled/thumbnail-generator

# Recargar systemd
sudo systemctl daemon-reload

# Recargar nginx
sudo systemctl reload nginx 2>/dev/null || echo "Nginx no se pudo recargar"

# Eliminar directorio del proyecto
echo "🗂️  Eliminando directorio del proyecto..."
sudo rm -rf /home/germanmallo/auto_thumbnail

# Limpiar paquetes no necesarios
echo "🧽 Limpiando paquetes..."
sudo apt autoremove -y 2>/dev/null || echo "Limpieza automática completada"

echo "✅ Limpieza completada. Listo para Docker."