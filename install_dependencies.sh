#!/bin/bash
# Script de instalación de dependencias para el generador de thumbnails

echo "=== Instalando dependencias para Generador de Thumbnails ==="

# Actualizar pip
python3 -m pip install --upgrade pip

# Instalar librerías principales
python3 -m pip install Pillow>=10.0.0
python3 -m pip install requests>=2.31.0

echo "✓ Dependencias instaladas correctamente"
echo ""
echo "🎨 FORMAS DE USAR EL GENERADOR:"
echo ""
echo "1️⃣ MODO INTERACTIVO (Recomendado):"
echo "   python3 generate_thumbnail.py"
echo "   📝 Te guía paso a paso solicitando cada dato"
echo ""
echo "2️⃣ MODO POR ARGUMENTOS:"
echo "   python3 generate_thumbnail.py [imagen] [titulo] [icono1] [icono2] ..."
echo ""
echo "3️⃣ EJEMPLOS INCLUIDOS:"
echo "   python3 ejemplos.py"
echo ""
echo "📋 EJEMPLOS DE USO:"
echo ""
echo "🔸 Con argumentos:"
echo "  python3 generate_thumbnail.py 'fondo.jpg' 'Mi Tutorial' 'icon1.png'"
echo ""
echo "🔸 Con URLs:"
echo "  python3 generate_thumbnail.py \\"
echo "    'https://picsum.photos/1920/1080' \\"
echo "    'Tutorial Python' \\"
echo "    'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg'"
echo ""
echo "¡Listo para generar thumbnails increíbles! 🚀"
