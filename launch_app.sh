#!/bin/bash
# Acceso directo para Thumbnail Generator Web App

# Cambiar al directorio de la aplicación
cd "$(dirname "$0")"

# Activar entorno virtual si existe
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Ejecutar aplicación
echo "🎨 Iniciando Thumbnail Generator..."
echo "📱 La aplicación se abrirá en tu navegador en unos segundos..."

# Iniciar la aplicación web
python3 web_app.py

echo "👋 ¡Hasta la próxima!"
