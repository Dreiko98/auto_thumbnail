#!/bin/bash
# Instalador automático con entorno virtual

echo "=== Instalando dependencias para Generador de Thumbnails ==="

# Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv .venv
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source .venv/bin/activate

# Actualizar pip
echo "⬆️ Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -r requirements.txt

echo "✓ Dependencias instaladas correctamente"
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
