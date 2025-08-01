#!/bin/bash

# Script de despliegue para Netlify
# ================================

echo "🚀 PREPARANDO DESPLIEGUE PARA NETLIFY"
echo "====================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar pasos
show_step() {
    echo -e "\n${BLUE}📋 $1${NC}"
}

show_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

show_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

show_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "netlify.toml" ]; then
    show_error "Error: No estás en el directorio netlify_version"
    echo "Ejecuta: cd netlify_version && ./deploy.sh"
    exit 1
fi

show_step "Verificando archivos necesarios..."

# Verificar archivos críticos
required_files=("index.html" "js/thumbnail-generator.js" "js/app.js" "netlify.toml")
missing_files=()

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        show_success "$file encontrado"
    else
        missing_files+=("$file")
        show_error "$file no encontrado"
    fi
done

if [ ${#missing_files[@]} -gt 0 ]; then
    show_error "Faltan archivos críticos. No se puede continuar."
    exit 1
fi

show_step "Creando archivo de configuración de build..."

# Crear _redirects para Netlify (backup del netlify.toml)
cat > _redirects << EOF
/*    /index.html   200
EOF

show_success "_redirects creado"

show_step "Optimizando archivos para producción..."

# Minificar CSS inline (básico)
if command -v sed >/dev/null 2>&1; then
    # Crear backup
    cp index.html index.html.backup
    
    # Remover comentarios CSS y espacios extra (básico)
    sed -i 's/\/\*.*\*\///g' index.html
    show_success "CSS optimizado"
fi

show_step "Creando archivo ZIP para despliegue manual..."

# Crear ZIP excluyendo archivos innecesarios
zip -r ../thumbnail-generator-netlify.zip . \
    -x "*.backup" \
    -x "deploy.sh" \
    -x ".git/*" \
    -x "node_modules/*" \
    -x "*.log"

if [ $? -eq 0 ]; then
    show_success "ZIP creado: ../thumbnail-generator-netlify.zip"
else
    show_error "Error creando ZIP"
fi

show_step "Verificando configuración de AdSense..."

# Verificar que los placeholders de AdSense están presentes
if grep -q "ca-pub-XXXXXXXXXX" index.html; then
    show_warning "Recuerda actualizar los códigos de AdSense:"
    echo "  - Reemplaza 'ca-pub-XXXXXXXXXX' con tu Publisher ID"
    echo "  - Reemplaza 'data-ad-slot=\"XXXXXXXXXX\"' con tus Slot IDs"
else
    show_success "Códigos de AdSense configurados"
fi

echo ""
echo "🎯 OPCIONES DE DESPLIEGUE:"
echo "========================="

echo ""
echo "📦 OPCIÓN 1: Despliegue Drag & Drop"
echo "-----------------------------------"
echo "1. Ve a https://netlify.com"
echo "2. Arrastra el archivo '../thumbnail-generator-netlify.zip' a la zona de despliegue"
echo "3. ¡Listo! Tu app estará disponible en unos minutos"

echo ""
echo "🔗 OPCIÓN 2: Despliegue desde Git"
echo "--------------------------------"
echo "1. Sube este código a GitHub:"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Thumbnail Generator for Netlify'"
echo "   git branch -M main"
echo "   git remote add origin https://github.com/TU-USUARIO/thumbnail-generator.git"
echo "   git push -u origin main"
echo ""
echo "2. En Netlify:"
echo "   - New site from Git"
echo "   - Selecciona tu repositorio"
echo "   - Build command: (vacío)"
echo "   - Publish directory: netlify_version"

echo ""
echo "💰 CONFIGURACIÓN ADSENSE:"
echo "========================"
echo "1. Solicita cuenta en https://adsense.google.com"
echo "2. Añade tu dominio de Netlify cuando esté desplegado"
echo "3. Una vez aprobado, actualiza los códigos en index.html"

echo ""
echo "📊 NEXT STEPS:"
echo "=============="
echo "- Configurar dominio personalizado (opcional)"
echo "- Configurar Google Analytics"
echo "- Optimizar SEO con contenido adicional"
echo "- Promocionar en redes sociales"

echo ""
show_success "¡Preparación completada! Tu app está lista para Netlify 🚀"

# Restaurar backup si existe
if [ -f "index.html.backup" ]; then
    mv index.html.backup index.html
    echo "Archivo original restaurado"
fi
