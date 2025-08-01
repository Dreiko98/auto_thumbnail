# 🎨 Generador Automático de Thumbnails

Aplicación completa para generar thumbnails profesionales de 1920×1080px para blogs y redes sociales. Disponible como **script de Python** y **aplicación web moderna**.

## 🚀 Modos de Uso

### 🌐 **Aplicación Web (Recomendado)**
Interfaz web moderna con drag & drop, vista previa en tiempo real y descarga directa.

```bash
# Inicio rápido
./launch_app.sh
# O manualmente
python3 web_app.py
```
**Luego abre:** `http://localhost:5000`

### 💻 **Script de Línea de Comandos**
Generación directa desde terminal para automatización y scripts.

```bash
python3 generate_thumbnail.py
```

## ✨ Características

- ✅ **Interfaz Web Moderna**: Drag & drop, vista previa, responsive
- ✅ **Script CLI**: Automatización y uso programático  
- ✅ **Redimensionado inteligente**: 1920×1080px con desenfoque gaussiano
- ✅ **Tipografía profesional**: Alliance No.2 Bold Italic con efectos avanzados
- ✅ **Iconos escalables**: Hasta 4 iconos con sombras profesionales
- ✅ **Descarga desde URLs**: Soporte para imágenes remotas
- ✅ **Exportación optimizada**: PNG + capas separadas (simulando PSD)
- ✅ **App de escritorio**: Empaquetable como ejecutable independiente

## 🎨 Efectos Profesionales Aplicados

### Texto:
- **Fuente en cursiva**: Alliance No.2 Bold Italic
- **Sombra paralela**: 85% opacidad, 9px distancia, 24% extensión, 40px tamaño
- **Sombra interior**: 45% opacidad, 30° ángulo, 8% tamaño
- **Ajuste dinámico**: Máximo 2 líneas, tamaño adaptativo

### Iconos:
- **Sombra paralela profesional**: 85% opacidad, efectos coherentes
- **Escalado inteligente**: Se adaptan según cantidad
- **Centrado perfecto**: Alineación horizontal automática

## 🛠️ Instalación

```bash
# Opción 1: Instalación automática
./install_dependencies.sh

# Opción 2: Manual
pip install -r requirements.txt

# Opción 3: Con entorno virtual (recomendado)
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

## 🚀 Uso

### 🌐 Aplicación Web (Interfaz Moderna)

```bash
# Inicio rápido con script
./launch_app.sh

# O manualmente
python3 web_app.py
```

**Características de la Web App:**
- 🖱️ **Drag & Drop**: Arrastra archivos directamente
- 👁️ **Vista previa**: Ve el resultado antes de descargar
- 📱 **Responsive**: Funciona en cualquier dispositivo
- ⚡ **Tiempo real**: Procesamiento instantáneo
- 📥 **Descarga directa**: Un clic para obtener el PNG

**Acceso:** `http://localhost:5000`

### 💻 Script de Línea de Comandos

### 💻 Script de Línea de Comandos

**Modo interactivo (más fácil):**
```bash
python3 generate_thumbnail.py
```
Te guiará paso a paso pidiendo:
- Imagen de fondo (local o URL)
- Título del thumbnail  
- Iconos opcionales
- Nombre del archivo de salida

**Modo con argumentos:**
```bash
python3 generate_thumbnail.py "imagen.jpg" "Mi Título" "icono1.png" "icono2.png"
```

**Ejecutar ejemplos predefinidos:**
```bash
python3 ejemplos.py
```

## 📦 Crear App de Escritorio

Para distribuir como aplicación independiente (sin requerir Python):

```bash
# 1. Ejecutar empaquetador
python3 build_desktop_app.py

# 2. Ejecutar app generada
# Linux/macOS: ./dist/ThumbnailGenerator  
# Windows: dist/ThumbnailGenerator.exe
```

**Ventajas:**
- 🚀 No requiere Python instalado
- 📁 Portable y distribuible  
- 🖥️ Integración nativa con el OS
- ⚡ Inicio rápido desde acceso directo

## 📁 Archivos Generados

- `thumbnail.png` - Imagen final optimizada (1920×1080px)
- `thumbnail_capas/` - Directorio con capas separadas:
  - `01_fondo_desenfocado.png` - Fondo procesado con desenfoque
  - `02_texto_info.txt` - Información y configuración del texto
  - `03_icono_01.png`, `03_icono_02.png`, etc. - Iconos individuales con efectos

## 🎯 Ejemplos de Uso

### Ejemplo Web App:
1. Abre `http://localhost:5000`
2. Arrastra imagen de fondo
3. Escribe: "Tutorial de Python Avanzado"  
4. Añade iconos: python.png, vscode.png
5. Clic en "Generar Thumbnail"
6. Descarga el resultado

### Ejemplo CLI Interactivo:
```bash
python3 generate_thumbnail.py
📸 Imagen de fondo: paisaje.jpg
📝 Título: Mi Blog de Tecnología  
🎯 Iconos: tech.png, code.png
💾 Nombre: mi_thumbnail
```

### Ejemplo con URLs:
```bash
python3 generate_thumbnail.py \
  "https://picsum.photos/1920/1080" \
  "Desarrollo Web Moderno" \
  "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg"
```

## ⚙️ Especificaciones Técnicas

- **Resolución**: 1920 × 1080 píxeles (Full HD)
- **Fondo**: Redimensionado + desenfoque gaussiano 20px
- **Fuente principal**: Alliance No.2 Bold Italic (cursiva) con fallback automático
- **Efectos texto**: Sombra paralela (85% opacidad) + sombra interior (45% opacidad)
- **Iconos**: Escalado dinámico, máx. 4 iconos, sombras profesionales
- **Formato salida**: PNG sin compresión + capas separadas
- **Ajuste inteligente**: Tamaño de fuente dinámico (máximo 2 líneas)

## 🛠️ Dependencias

- **Python 3.8+** (Core del sistema)
- **Pillow** (Manipulación de imágenes y efectos)
- **requests** (Descarga de imágenes desde URLs)
- **Flask** (Servidor web para interfaz moderna)
- **Werkzeug** (Utilidades para aplicación web)
- **PyInstaller** (Empaquetado como app de escritorio)

## 📚 Archivos del Proyecto

```
auto_thumbnail/
├── 📄 generate_thumbnail.py     # Motor principal de generación
├── 🌐 web_app.py               # Aplicación web Flask
├── 📱 templates/index.html      # Interfaz web moderna
├── 🚀 start_web_app.py         # Iniciador rápido web
├── 📦 build_desktop_app.py     # Empaquetador de escritorio
├── ⚡ launch_app.sh            # Acceso directo Linux/macOS
├── 🔧 install_dependencies.sh  # Instalador automático
├── 📋 requirements.txt         # Dependencias Python
├── 📖 README.md               # Documentación principal
├── 📚 WEB_APP_GUIDE.md        # Guía completa web app
└── 🧪 ejemplos.py             # Scripts de ejemplo CLI
```

## 🎉 Resultados

El generador crea thumbnails profesionales con:
- ✨ **Fondo desenfocado** manteniendo proporción original
- 📝 **Texto legible y estilizado** con efectos de sombra avanzados  
- 🎯 **Iconos centrados y proporcionados** con sombras coherentes
- 🚀 **Calidad optimizada** para web, redes sociales y presentaciones
- 📱 **Diseño responsive** que se ve bien en cualquier tamaño

## 🔗 Enlaces Útiles

- 📚 **[Guía Completa Web App](WEB_APP_GUIDE.md)** - Tutorial detallado de la interfaz web
- 🎨 **[Ejemplos CLI](ejemplos.py)** - Scripts de ejemplo para línea de comandos  
- ⚙️ **[Instalador](install_dependencies.sh)** - Script automático de dependencias
- 🖥️ **[Empaquetador](build_desktop_app.py)** - Crear app de escritorio

---

**🎨 ¡Crea thumbnails profesionales en segundos!** 🎨

*Compatible con Linux, macOS y Windows • Interfaz web moderna • App de escritorio distribuible*
