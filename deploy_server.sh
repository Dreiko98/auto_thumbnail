#!/bin/bash
# Script de despliegue para servidor Ubuntu
# Ejecutar como: bash deploy_server.sh

set -e

echo "🚀 DESPLIEGUE DE THUMBNAIL GENERATOR EN SERVIDOR"
echo "================================================="

# Variables
SERVER_USER="germanmallo"
PROJECT_DIR="/home/$SERVER_USER/auto_thumbnail"
SERVICE_NAME="thumbnail-generator"

echo "📋 PASO 1: Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

echo "🐍 PASO 2: Instalando dependencias del sistema..."
sudo apt install -y python3 python3-pip python3-venv nginx gunicorn python3-gunicorn

echo "📁 PASO 3: Creando directorio del proyecto..."
sudo mkdir -p $PROJECT_DIR
sudo chown $SERVER_USER:$SERVER_USER $PROJECT_DIR

echo "📦 PASO 4: Copiando archivos del proyecto..."
# Aquí necesitarás copiar los archivos desde tu máquina local al servidor
# Puedes usar scp o rsync para esto
echo "⚠️  IMPORTANTE: Copia todos los archivos del proyecto a $PROJECT_DIR"
echo "   Usa: scp -r /ruta/local/auto_thumbnail $SERVER_USER@100.87.242.53:$PROJECT_DIR"
read -p "Presiona Enter cuando hayas copiado los archivos..."

echo "🔧 PASO 5: Instalando dependencias de Python..."
cd $PROJECT_DIR
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt gunicorn

echo "⚙️  PASO 6: Configurando servicio systemd..."
sudo cp thumbnail-generator.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME

echo "🌐 PASO 7: Configurando Nginx..."
sudo cp nginx.conf /etc/nginx/sites-available/$SERVICE_NAME
sudo ln -sf /etc/nginx/sites-available/$SERVICE_NAME /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

echo "🔄 PASO 8: Iniciando servicios..."
sudo systemctl start $SERVICE_NAME
sudo systemctl status $SERVICE_NAME --no-pager

echo "🧹 PASO 9: Limpiando..."
# Remover configuración por defecto de nginx si existe
sudo rm -f /etc/nginx/sites-enabled/default

echo ""
echo "✅ DESPLIEGUE COMPLETADO"
echo "=========================="
echo "🌐 Tu aplicación está disponible en: http://100.87.242.53"
echo ""
echo "📊 Comandos útiles:"
echo "   • Ver logs: sudo journalctl -u $SERVICE_NAME -f"
echo "   • Reiniciar app: sudo systemctl restart $SERVICE_NAME"
echo "   • Reiniciar nginx: sudo systemctl reload nginx"
echo "   • Ver estado: sudo systemctl status $SERVICE_NAME"
echo ""
echo "🔒 Considera configurar SSL con Let's Encrypt para HTTPS"