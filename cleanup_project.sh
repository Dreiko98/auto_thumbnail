#!/bin/bash
# Script para limpiar archivos innecesarios del proyecto

echo "🧹 Limpiando proyecto para uso local..."

# Archivos y carpetas a eliminar
FILES_TO_DELETE=(
    "WEB_APP_GUIDE.md"
    "build_desktop_app.py"
    "start_web_app.py"
    "ejemplos.py"
    "config.json"
    "thumbnail-generator-netlify.zip"
    "netlify_version/"
    "uploads/"
    "generated_thumbnails/"
    "__pycache__/"
    ".git/"
    "venv/"
    ".venv/"
    "=10.0.0"
    "=2.31.0"
)

# Archivos de ejemplo/test a eliminar
EXAMPLE_FILES=(
    "ejemplo.png"
    "ejemplo2.png"
    "holaa.png"
    "icon.png"
    "final_test.jpg"
    "final_test.png"
    "test_final.jpg"
    "test_final.png"
    "thumbnail.png"
    "Letra nueva.png"
    "prueba desde casa.png"
    "prueba larga.png"
    "pruebaaa.png"
)

# Carpetas de capas de ejemplo
LAYER_FOLDERS=(
    "ejemplo2_capas/"
    "holaa_capas/"
    "Letra nueva_capas/"
    "prueba desde casa_capas/"
    "prueba larga_capas/"
    "pruebaaa_capas/"
    "thumbnail_capas/"
)

# Eliminar archivos principales
for file in "${FILES_TO_DELETE[@]}"; do
    if [ -e "$file" ]; then
        rm -rf "$file"
        echo "❌ Eliminado: $file"
    fi
done

# Eliminar archivos de ejemplo
for file in "${EXAMPLE_FILES[@]}"; do
    if [ -e "$file" ]; then
        rm -f "$file"
        echo "❌ Eliminado: $file"
    fi
done

# Eliminar carpetas de capas
for folder in "${LAYER_FOLDERS[@]}"; do
    if [ -d "$folder" ]; then
        rm -rf "$folder"
        echo "❌ Eliminado: $folder"
    fi
done

echo ""
echo "✅ Limpieza completada!"
echo ""
echo "📁 Archivos restantes (esenciales):"
ls -la | grep -E '\.(py|sh|txt|md|html)$|templates'
echo ""
echo "🚀 Para usar el proyecto:"
echo "   1. ./install_dependencies.sh"
echo "   2. ./launch_app.sh"
echo "   3. Abrir http://localhost:5000"
