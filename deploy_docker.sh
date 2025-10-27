#!/bin/bash
# Despliegue con Docker - Script completo
# Uso: ./deploy_docker.sh

set -e

echo "🐳 DESPLIEGUE CON DOCKER - THUMBNAIL GENERATOR"
echo "=============================================="

# Función de limpieza
cleanup_previous_deployment() {
    echo "🧹 PASO 1: Limpiando despliegue anterior..."

    # Detener y eliminar servicios systemd
    sudo systemctl stop thumbnail-generator 2>/dev/null || true
    sudo systemctl disable thumbnail-generator 2>/dev/null || true
    sudo rm -f /etc/systemd/system/thumbnail-generator.service
    sudo systemctl daemon-reload

    # Eliminar configuración nginx
    sudo rm -f /etc/nginx/sites-available/thumbnail-generator
    sudo rm -f /etc/nginx/sites-enabled/thumbnail-generator
    sudo systemctl reload nginx 2>/dev/null || true

    # Limpiar archivos del proyecto anterior
    sudo rm -rf /home/germanmallo/auto_thumbnail 2>/dev/null || true

    echo "✅ Limpieza completada"
}

# Instalar Docker si no está instalado
install_docker() {
    echo "🐳 PASO 2: Instalando Docker..."

    if ! command -v docker &> /dev/null; then
        sudo apt update
        sudo apt install -y docker.io docker-compose-plugin
        sudo systemctl start docker
        sudo systemctl enable docker

        # Agregar usuario al grupo docker
        sudo usermod -aG docker germanmallo
        echo "⚠️  IMPORTANTE: Cierra sesión y vuelve a conectarte para usar Docker sin sudo"
    else
        echo "✅ Docker ya está instalado"
    fi
}

# Configurar firewall
configure_firewall() {
    echo "🔥 PASO 3: Configurando firewall..."

    # Permitir puerto 80
    sudo ufw allow 80/tcp 2>/dev/null || true
    sudo ufw allow 22/tcp 2>/dev/null || true
    sudo ufw --force enable 2>/dev/null || true

    echo "✅ Firewall configurado"
}

# Desplegar con Docker
deploy_with_docker() {
    echo "🚀 PASO 4: Desplegando con Docker..."

    # Crear directorio si no existe
    mkdir -p /home/germanmallo/auto_thumbnail

    # Copiar archivos del proyecto (esto debe hacerse desde la máquina local)
    echo "📦 Copiando archivos del proyecto..."
    echo "⚠️  Asegúrate de haber copiado los archivos desde tu máquina local:"
    echo "   scp -r /home/dreiko98/Escritorio/auto_thumbnail germanmallo@100.87.242.53:~/auto_thumbnail"

    # Verificar que los archivos estén presentes
    if [ ! -f "docker-compose.yml" ]; then
        echo "❌ Error: docker-compose.yml no encontrado. Copia los archivos primero."
        exit 1
    fi

    # Crear directorios necesarios
    mkdir -p uploads thumbnails

    # Construir e iniciar contenedores
    echo "🔨 Construyendo imagen Docker..."
    sudo docker-compose build

    echo "🚀 Iniciando servicios..."
    sudo docker-compose up -d

    echo "⏳ Esperando a que los servicios estén listos..."
    sleep 10

    # Verificar que esté funcionando
    if curl -f http://localhost/health &>/dev/null; then
        echo "✅ Despliegue exitoso"
    else
        echo "❌ Error en el despliegue. Revisando logs..."
        sudo docker-compose logs
        exit 1
    fi
}

# Mostrar información final
show_info() {
    echo ""
    echo "🎉 ¡DESPLIEGUE COMPLETADO!"
    echo "=========================="
    echo "🌐 URL de acceso: http://100.87.242.53"
    echo ""
    echo "📊 Comandos útiles:"
    echo "   • Ver logs: sudo docker-compose logs -f"
    echo "   • Detener: sudo docker-compose down"
    echo "   • Reiniciar: sudo docker-compose restart"
    echo "   • Actualizar: sudo docker-compose pull && sudo docker-compose up -d"
    echo ""
    echo "🔍 Verificar estado:"
    echo "   • sudo docker ps"
    echo "   • curl http://localhost/health"
    echo ""
    echo "💡 Para SSL con Let's Encrypt:"
    echo "   sudo apt install certbot"
    echo "   sudo certbot --nginx -d tudominio.com"
}

# Ejecutar pasos
cleanup_previous_deployment
install_docker
configure_firewall
deploy_with_docker
show_info