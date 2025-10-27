#!/bin/bash
# Instalador automático con entorno virtual

set -e  # Salir si hay error

echo "=== Instalando dependencias para Generador de Thumbnails ==="

# Verificar si ya estamos en un entorno virtual
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "⚠️  Ya hay un entorno virtual activo. Desactivando..."
    deactivate 2>/dev/null || true
fi

# Crear entorno virtual si no existe o recrear si está corrupto
if [ ! -d ".venv" ] || [ ! -f ".venv/bin/activate" ]; then
    echo "📦 Creando entorno virtual..."
    rm -rf .venv 2>/dev/null || true
    python3 -m venv .venv
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source .venv/bin/activate

# Verificar que estamos en el entorno virtual
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "❌ Error: No se pudo activar el entorno virtual"
    exit 1
fi

# Actualizar pip
echo "⬆️ Actualizando pip..."
pip install --upgrade pip --break-system-packages

# Instalar dependencias
echo "📚 Instalando dependencias..."
if pip install -r requirements.txt --break-system-packages; then
    echo "✓ Dependencias instaladas correctamente"
else
    echo "❌ Error instalando dependencias"
    exit 1
fi

echo ""
echo "🎨 FORMAS DE USAR EL GENERADOR:"
echo ""
echo "1️⃣ APLICACIÓN WEB (Recomendado):"
echo "   ./launch_app.sh"
echo "   📱 Interfaz moderna en http://localhost:5000"
echo ""
echo "2️⃣ SCRIPT CLI:"
echo "   source .venv/bin/activate"
echo "   python3 generate_thumbnail.py"
echo ""
echo "¡Listo para generar thumbnails increíbles! 🚀"
