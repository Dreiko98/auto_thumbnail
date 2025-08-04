#!/bin/bash
# Acceso directo para Thumbnail Generator Web App

# Cambiar al directorio de la aplicación
cd "$(dirname "$0")"

# Activar entorno virtual
if [ -d ".venv" ]; then
    echo "🔄 Activando entorno virtual..."
    source .venv/bin/activate
else
    echo "⚠️  Entorno virtual no encontrado. Ejecuta ./install_dependencies.sh primero"
    exit 1
fi

# Ejecutar aplicación
echo "🎨 Iniciando Thumbnail Generator..."
echo "📱 La aplicación se abrirá en tu navegador en unos segundos..."

# Iniciar la aplicación web
python3 web_app.py

echo "👋 ¡Hasta la próxima!"
