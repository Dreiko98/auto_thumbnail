#!/bin/bash
# Script para copiar el proyecto al servidor
# Uso: ./deploy_to_server.sh

set -e

SERVER_USER="germanmallo"
SERVER_IP="100.87.242.53"
PROJECT_DIR="/home/dreiko98/Escritorio/auto_thumbnail"

echo "📤 COPIANDO PROYECTO AL SERVIDOR"
echo "================================="

echo "🔄 Copiando archivos..."
rsync -avz --exclude='.venv' --exclude='__pycache__' --exclude='*.pyc' \
    -e ssh $PROJECT_DIR $SERVER_USER@$SERVER_IP:~/auto_thumbnail

echo "✅ Archivos copiados exitosamente"
echo ""
echo "🖥️  PRÓXIMOS PASOS EN EL SERVIDOR:"
echo "   ssh $SERVER_USER@$SERVER_IP"
echo "   cd auto_thumbnail"
echo "   ./deploy_server.sh"