#!/bin/bash
#############################################
# Script de Deployment para Thumbnail Generator
# Con autenticación, gestión de usuarios y limpieza automática
#############################################

set -e  # Salir si hay algún error

echo "🚀 INICIANDO DEPLOYMENT DE THUMBNAIL GENERATOR"
echo "================================================"

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# 1. Verificar que estamos en el directorio correcto
if [ ! -f "docker-compose.yml" ]; then
    print_error "No se encuentra docker-compose.yml"
    print_info "Asegúrate de estar en el directorio del proyecto"
    exit 1
fi

print_success "Directorio del proyecto verificado"

# 2. Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    print_warning "Archivo .env no encontrado, creando uno nuevo..."
    
    # Generar secret key segura
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    
    cat > .env << EOF
# Configuración generada automáticamente
FLASK_SECRET_KEY=${SECRET_KEY}
DATABASE_PATH=/app/db_data/thumbnail_users.db
EOF
    
    print_success "Archivo .env creado con clave segura"
else
    print_info "Usando archivo .env existente"
fi

# 3. Detener contenedores si están corriendo
print_info "Deteniendo contenedores existentes..."
docker-compose down 2>/dev/null || true
print_success "Contenedores detenidos"

# 4. Construir imágenes
print_info "Construyendo imágenes Docker..."
docker-compose build --no-cache
print_success "Imágenes construidas"

# 5. Iniciar servicios
print_info "Iniciando servicios..."
docker-compose up -d
print_success "Servicios iniciados"

# 6. Esperar a que los servicios estén listos
print_info "Esperando a que los servicios estén listos..."
sleep 5

# 7. Verificar estado de los servicios
print_info "Verificando estado de los servicios..."

if docker ps | grep -q "thumbnail-app"; then
    print_success "Contenedor thumbnail-app: CORRIENDO"
else
    print_error "Contenedor thumbnail-app: NO ESTÁ CORRIENDO"
    docker logs thumbnail-app
    exit 1
fi

if docker ps | grep -q "thumbnail-nginx"; then
    print_success "Contenedor thumbnail-nginx: CORRIENDO"
else
    print_warning "Contenedor thumbnail-nginx: NO ESTÁ CORRIENDO"
fi

# 8. Probar health check
print_info "Probando health check..."
sleep 3

if curl -f http://localhost:5000/health > /dev/null 2>&1; then
    print_success "Health check: OK"
else
    print_error "Health check: FALLO"
    print_info "Logs del contenedor:"
    docker logs thumbnail-app --tail 50
    exit 1
fi

# 9. Mostrar información de acceso
echo ""
echo "================================================"
echo -e "${GREEN}✓ DEPLOYMENT COMPLETADO EXITOSAMENTE${NC}"
echo "================================================"
echo ""
echo "📱 Acceso a la aplicación:"
echo "   • Aplicación directa: http://localhost:5000"
echo "   • A través de Nginx:  http://localhost:8080"
echo ""
echo "🔧 Comandos útiles:"
echo "   • Ver logs:           docker-compose logs -f"
echo "   • Ver logs de app:    docker-compose logs -f app"
echo "   • Reiniciar:          docker-compose restart"
echo "   • Detener:            docker-compose down"
echo ""
echo "💾 Base de datos:"
echo "   • La base de datos se guarda en un volumen persistente"
echo "   • Los usuarios, contraseñas y tokens se mantienen entre reinicios"
echo "   • Ubicación: Docker volume 'thumbnail_db'"
echo ""
echo "🗑️ Limpieza de archivos:"
echo "   • Los archivos temporales se limpian automáticamente"
echo "   • Solo se persiste la base de datos de usuarios"
echo "   • Las imágenes subidas/generadas se eliminan después de usarse"
echo ""
echo "================================================"

# 10. Opcional: Mostrar logs en tiempo real
read -p "¿Quieres ver los logs en tiempo real? (s/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[SsYy]$ ]]; then
    docker-compose logs -f
fi
