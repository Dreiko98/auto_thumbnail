#!/bin/bash
# Acceso directo para Thumbnail Generator Web App

set -e  # Salir si hay error

# Cambiar al directorio de la aplicación
cd "$(dirname "$0")"

# Verificar si ya estamos en un entorno virtual
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "⚠️  Ya hay un entorno virtual activo. Desactivando..."
    deactivate 2>/dev/null || true
fi

# Activar entorno virtual
if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
    echo "🔄 Activando entorno virtual..."
    source .venv/bin/activate
else
    echo "⚠️  Entorno virtual no encontrado. Ejecuta ./install_dependencies.sh primero"
    exit 1
fi

# Verificar que estamos en el entorno virtual
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "❌ Error: No se pudo activar el entorno virtual"
    exit 1
fi

# Ejecutar aplicación
echo "🎨 Iniciando Thumbnail Generator..."
echo "📱 La aplicación se abrirá en tu navegador en unos segundos..."

# Iniciar la aplicación web
python3 web_app.py

echo "👋 ¡Hasta la próxima!"
