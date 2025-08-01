#!/bin/bash

# Script de despliegue para Netlify con Backend Python
# ==================================================

echo "🚀 PREPARANDO DESPLIEGUE PARA NETLIFY (con Python Backend)"
echo "=========================================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar pasos
show_step() {
    echo -e "${BLUE}📋 $1${NC}"
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
    show_error "No se encontró netlify.toml. Ejecuta desde netlify_version/"
    exit 1
fi

show_step "Verificando archivos necesarios..."

# Verificar archivos críticos
required_files=(
    "index.html"
    "netlify.toml"
    "requirements.txt"
    "netlify/functions/generate_thumbnail.py"
    "js/app.js"
    "js/thumbnail-generator.js"
)

missing_files=()
for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        show_success "✓ $file"
    else
        show_error "✗ $file"
        missing_files+=("$file")
    fi
done

if [[ ${#missing_files[@]} -gt 0 ]]; then
    show_error "Faltan archivos críticos. No se puede desplegar."
    exit 1
fi

show_step "Verificando función serverless..."

# Verificar que la función Python esté correcta
if grep -q "def handler" netlify/functions/generate_thumbnail.py; then
    show_success "Función Python válida"
else
    show_error "Función Python inválida"
    exit 1
fi

show_step "Optimizando archivos..."

# Verificar tamaño de archivos
total_size=$(du -sh . | cut -f1)
show_success "Tamaño total del proyecto: $total_size"

show_step "Verificando configuración de AdSense..."

# Verificar que AdSense esté configurado
if grep -q "ca-pub-6506999020999478" index.html; then
    show_success "AdSense configurado correctamente"
else
    show_warning "AdSense no encontrado - no podrás monetizar"
fi

show_step "Preparando para despliegue..."

# Crear archivo de información del build
cat > build-info.json << EOF
{
    "build_date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "version": "2.0.0-serverless",
    "backend": "Python Netlify Functions",
    "features": [
        "Python backend con Pillow",
        "Efectos profesionales",
        "Google AdSense",
        "Canvas frontend",
        "Drag & drop"
    ]
}
EOF

show_success "Build info creado"

echo ""
echo "🎯 INFORMACIÓN DE DESPLIEGUE"
echo "============================"
echo "📁 Directorio: $(pwd)"
echo "🔧 Backend: Python Netlify Functions"
echo "💰 Monetización: Google AdSense"
echo "📊 Archivos: $(find . -name "*.html" -o -name "*.js" -o -name "*.py" | wc -l) archivos"
echo ""

show_step "Instrucciones de despliegue:"
echo ""
echo "1. 📤 SUBIDA MANUAL:"
echo "   - Comprimir toda la carpeta netlify_version en un ZIP"
echo "   - Ir a netlify.com → Sites → Deploy manually"
echo "   - Arrastrar el ZIP"
echo ""
echo "2. 🔗 DESDE GITHUB:"
echo "   - git add ."
echo "   - git commit -m 'Deploy with Python backend'"
echo "   - git push origin main"
echo "   - Conectar repo en netlify.com"
echo "   - Build directory: netlify_version"
echo ""
echo "3. 🌐 CONFIGURACIÓN EN NETLIFY:"
echo "   - Functions directory: netlify/functions"
echo "   - Python version: 3.8"
echo "   - Install command: pip install -r requirements.txt"
echo ""

show_success "¡Listo para desplegar! 🚀"
echo ""
echo "💡 URLs importantes:"
echo "   • Netlify: https://app.netlify.com/"
echo "   • Google AdSense: https://www.google.com/adsense/"
echo "   • Docs Functions: https://docs.netlify.com/functions/overview/"
