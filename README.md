# 🎨 Generador Automático de Thumbnails

Aplicación para generar thumbnails profesionales de 1920×1080px. Disponible como **script de Python** y **aplicación web**.

## 🚀 Inicio Rápido

### 🌐 **Aplicación Web (Recomendado)**
```bash
# Instalación automática
./install_dependencies.sh

# Ejecutar aplicación web
./launch_app.sh
# O manualmente: python3 web_app.py
```
**Abre:** `http://localhost:5000`

### 💻 **Script de Línea de Comandos**
```bash
python3 generate_thumbnail.py
```

## ✨ Características

- ✅ **Interfaz Web**: Drag & drop, vista previa
- ✅ **Script CLI**: Uso desde terminal
- ✅ **Redimensionado inteligente**: 1920×1080px con desenfoque
- ✅ **Tipografía profesional**: Fuentes cursivas con efectos
- ✅ **Iconos escalables**: Hasta 4 iconos con sombras
- ✅ **Soporte URLs**: Descarga imágenes remotas
- ✅ **Exportación**: PNG + capas separadas

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

### 🌐 Aplicación Web
```bash
# Inicio rápido
./launch_app.sh

# O manualmente
python3 web_app.py
```
**Acceso:** `http://localhost:5000`

**Características:**
- 🖱️ **Drag & Drop**: Arrastra archivos directamente
- 👁️ **Vista previa**: Ve el resultado antes de descargar
- 📥 **Descarga directa**: Un clic para obtener el PNG

### 💻 Script CLI

**Modo interactivo:**
```bash
python3 generate_thumbnail.py
```

**Con argumentos:**
```bash
python3 generate_thumbnail.py "imagen.jpg" "Mi Título" "icono1.png" "icono2.png"
```

##  Archivos Generados

- `thumbnail.png` - Imagen final (1920×1080px)
- `thumbnail_capas/` - Capas separadas:
  - `01_fondo_desenfocado.png`
  - `02_texto_info.txt`
  - `03_icono_01.png`, etc.

## ️ Dependencias

- **Python 3.8+**
- **Pillow** (manipulación de imágenes)
- **requests** (descarga de URLs)
- **Flask** (aplicación web)

## 📚 Archivos del Proyecto

```
auto_thumbnail/
├── generate_thumbnail.py     # Motor principal
├── web_app.py               # Aplicación web
├── templates/index.html     # Interfaz web
├── requirements.txt         # Dependencias
├── install_dependencies.sh  # Instalador
├── launch_app.sh           # Lanzador
└── README.md               # Esta guía
```

---

**🎨 ¡Crea thumbnails profesionales en segundos!** 🎨
