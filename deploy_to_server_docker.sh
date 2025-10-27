#!/bin/bash
# Script para copiar proyecto al servidor para despliegue con Docker
# Uso: ./deploy_to_server_docker.sh

set -e

SERVER_USER="germanmallo"
SERVER_IP="100.87.242.53"
PROJECT_DIR="/home/dreiko98/Escritorio/auto_thumbnail"

echo "🐳 COPIANDO PROYECTO AL SERVIDOR (DOCKER)"
echo "========================================="

echo "📤 Copiando archivos..."
rsync -avz --exclude='.venv' --exclude='__pycache__' --exclude='*.pyc' \
    --exclude='.git' --exclude='uploads' --exclude='thumbnails' \
    -e ssh $PROJECT_DIR $SERVER_USER@$SERVER_IP:~/auto_thumbnail

echo "✅ Archivos copiados exitosamente"
echo ""
echo "🖥️  PRÓXIMOS PASOS EN EL SERVIDOR:"
echo "   ssh $SERVER_USER@$SERVER_IP"
echo "   cd auto_thumbnail"
echo "   chmod +x deploy_docker.sh"
echo "   ./deploy_docker.sh"